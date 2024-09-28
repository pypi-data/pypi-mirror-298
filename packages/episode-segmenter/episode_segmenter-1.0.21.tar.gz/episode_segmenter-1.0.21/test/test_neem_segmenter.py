import os

from neem_pycram_interface import PyCRAMNEEMInterface

from episode_segmenter.event_detectors import AgentPickUpDetector
from episode_segmenter.neem_segmenter import NEEMSegmenter
from unittest import TestCase

from pycram.datastructures.enums import WorldMode
from pycram.ros.viz_marker_publisher import VizMarkerPublisher
from pycram.datastructures.world import World
from pycram.worlds.bullet_world import BulletWorld


class TestNEEMSegmentor(TestCase):
    ns: NEEMSegmenter
    viz_mark_publisher: VizMarkerPublisher

    @classmethod
    def setUpClass(cls):
        BulletWorld(WorldMode.GUI)
        pni = PyCRAMNEEMInterface(f'mysql+pymysql://{os.environ["my_maria_uri"]}')
        cls.ns = NEEMSegmenter(pni, detectors_to_start=[AgentPickUpDetector], annotate_events=True)
        cls.viz_mark_publisher = VizMarkerPublisher()

    @classmethod
    def tearDownClass(cls):
        cls.viz_mark_publisher._stop_publishing()
        if World.current_world is not None:
            World.current_world.exit()
        cls.ns.join()

    def test_event_detector(self):
        self.ns.run_event_detectors_on_neem([17])
