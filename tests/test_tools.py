import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
ann=module("annotate",ROOT/"skills/design-spec/scripts/annotate.py")
val=module("validate",ROOT/"skills/design-spec/scripts/validate_report.py")
ins=module("installer",ROOT/"install.py")

class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name).resolve()
        Image.new("RGB",(400,250),"#17212c").save(self.base/"original.png")
        self.marks={"image_size":[400,250],"marks":[
            {"id":"E01","shape":"rect","bbox":[20,40,180,100]}]}
        (self.base/"marks.json").write_text(json.dumps(self.marks))
        ann.annotate(self.base/"original.png",self.base/"marks.json",self.base/"marked.png")
        self.data={"version":"1.0","url":"https://example.test",
          "inspected_at":"2026-11-10T12:00:00+00:00","scope":"Synthetic fixture",
          "annotation_status":"complete","evidence":[
            {"id":"S01","kind":"screenshot","path":"original.png",
             "annotated_path":"marked.png","marks_path":"marks.json",
             "viewport":"400x250","state":"default","item_ids":["E01"]}],
          "items":[{"id":"E01","name":"Card","location":"Main","description":"A panel",
                    "category":"component","term_kind":"established","status":"observed",
                    "evidence":["S01"],"specs":{},"motion":None}],
          "coverage":[{"route":"/","section":"Main","viewport":"desktop","state":"default",
                       "status":"inspected","evidence":["S01"],"notes":""}],
          "limitations":[],"sources":[]}

    def test_valid_inventory(self):
        self.assertEqual(val.validate(self.data,self.base),[])

    def test_original_preserved_and_marked(self):
        original=Image.open(self.base/"original.png")
        marked=Image.open(self.base/"marked.png")
        self.assertEqual(original.size,marked.size)
        self.assertEqual(original.getpixel((20,40)),(23,33,44))
        self.assertNotEqual(original.getpixel((20,40)),marked.getpixel((20,40)))

    def test_bounds_and_dimension_mismatch(self):
        for update in ({"image_size":[800,500]},
                       {"marks":[{"id":"E01","shape":"ellipse","bbox":[390,20,50,50]}]}):
            marks={**self.marks,**update}
            (self.base/"bad.json").write_text(json.dumps(marks))
            with self.assertRaises(ValueError):
                ann.annotate(self.base/"original.png",self.base/"bad.json",self.base/"new.png")
        self.assertFalse((self.base/"new.png").exists())

    def test_manual_label_position(self):
        marks=copy.deepcopy(self.marks)
        marks["marks"][0]["label_xy"]=[250,10]
        (self.base/"custom.json").write_text(json.dumps(marks))
        ann.annotate(self.base/"original.png",self.base/"custom.json",self.base/"custom.png")
        self.assertTrue((self.base/"custom.png").is_file())
        marks["marks"][0]["label_xy"]=[399,249]
        (self.base/"custom.json").write_text(json.dumps(marks))
        with self.assertRaises(ValueError):
            ann.annotate(self.base/"original.png",self.base/"custom.json",self.base/"bad-label.png")
        self.assertFalse((self.base/"bad-label.png").exists())

    def test_refuse_overwrite(self):
        before=(self.base/"marked.png").read_bytes()
        with self.assertRaises(ValueError):
            ann.annotate(self.base/"original.png",self.base/"marks.json",self.base/"marked.png")
        self.assertEqual(before,(self.base/"marked.png").read_bytes())

    def test_missing_reference_and_marks(self):
        self.data["items"][0]["evidence"]=["missing"]
        errors=val.validate(self.data,self.base)
        self.assertTrue(any("missing evidence" in e for e in errors))
        self.assertTrue(any("no screenshot marks" in e for e in errors))

    def test_reject_fake_image(self):
        (self.base/"original.png").write_text("Not a screenshot")
        self.assertTrue(any("not a valid image" in e for e in val.validate(self.data,self.base)))

    def test_reject_escaping_path(self):
        self.data["evidence"][0]["path"]="../outside.png"
        self.assertTrue(any("stay inside" in e for e in val.validate(self.data,self.base)))

    def test_reject_wrong_mark_dimensions(self):
        marks=copy.deepcopy(self.marks)
        marks["image_size"]=[800,500]
        (self.base/"marks.json").write_text(json.dumps(marks))
        self.assertTrue(any("dimensions differ" in e for e in val.validate(self.data,self.base)))

    def make_motion(self):
        self.data["items"][0].update(id="M01",category="motion",motion={
            "trigger":"hover","behavior":"scale","properties":["transform"],
            "duration_ms":240,"duration_source":"Computed CSS","easing":"ease-out",
            "repeat":"on pointer entry","reduced_motion":"not tested"})
        self.data["evidence"][0]["item_ids"]=["M01"]
        self.marks["marks"][0]["id"]="M01"
        (self.base/"marks.json").write_text(json.dumps(self.marks))

    def test_single_frame_is_not_motion(self):
        self.make_motion()
        self.assertTrue(any("two distinct" in e for e in val.validate(self.data,self.base)))

    def test_viewport_mismatch_and_identical_frames(self):
        self.make_motion()
        (self.base/"second.png").write_bytes((self.base/"original.png").read_bytes())
        second={**self.data["evidence"][0],"id":"S02","path":"second.png","viewport":"390x844"}
        self.data["evidence"].append(second)
        self.data["items"][0]["evidence"].append("S02")
        errors=val.validate(self.data,self.base)
        self.assertTrue(any("same viewport" in e for e in errors))
        self.assertTrue(any("identical frame" in e for e in errors))

    def test_measured_spec_requires_source(self):
        self.data["items"][0]["specs"]={"radius":{"value":24,"unit":"px","status":"measured"}}
        self.assertTrue(any("requires source" in e for e in val.validate(self.data,self.base)))

    def test_installer_preserves_conflicts(self):
        dest=self.base/"skills/design-spec"
        dest.mkdir(parents=True)
        (dest/"SKILL.md").write_text("User's existing skill")
        with self.assertRaises(ValueError): ins.install([dest])
        self.assertEqual((dest/"SKILL.md").read_text(),"User's existing skill")

    def test_install_dry_run_and_idempotency(self):
        dest=self.base/"skills/design-spec"
        ins.install([dest],dry_run=True)
        self.assertFalse(dest.exists())
        ins.install([dest])
        self.assertTrue((dest/"references/output.md").is_file())
        ins.install([dest])

    def test_destination_selection(self):
        paths=ins.destinations("all",self.base)
        self.assertEqual(paths,[self.base/".claude/skills/design-spec",
                                self.base/".agents/skills/design-spec"])
        with self.assertRaises(ValueError): ins.destinations("generic")

if __name__=="__main__": unittest.main()
