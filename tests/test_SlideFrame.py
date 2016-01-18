from mc.uix.slide_frame import SlideFrame, SlideFrameParent
from .MpfMcTestCase import MpfMcTestCase


class TestSlideFrame(MpfMcTestCase):
    def get_machine_path(self):
        return 'tests/machine_files/slide_frame'

    def get_config_file(self):
        return 'test_slide_frame.yaml'

    def test_slide_frame(self):
        # put slide1 on the default displays
        self.mc.targets['default'].add_slide(name='slide1',
                                             config=self.mc.slide_configs[
                                                 'slide1'])

        # it takes a few frames for new slide frames to initialize, so we have
        # to wait for that to be done and to get added to the list
        while len(self.mc.targets['default'].current_slide.children) == 1:
            self.advance_time(.01)

        # make sure our slide frame is a valid target
        self.assertIn('frame1', self.mc.targets)

        # the slide frame's parent should be a widget in slide1
        self.assertEqual(
                self.mc.targets['default'].current_slide.children[1].name,
                'frame1')

        # grab some references which are easy to follow
        default_frame = self.mc.targets['default']
        frame1_frame = self.mc.targets['frame1']
        default_frame_parent = self.mc.targets['default'].parent
        frame1_frame_parent = self.mc.targets['frame1'].parent

        # make sure they're right. :)
        self.assertEqual(default_frame.name, 'default')
        self.assertEqual(frame1_frame.name, 'frame1')
        self.assertEqual(default_frame_parent.name, 'default')
        self.assertEqual(frame1_frame_parent.name, 'frame1')
        self.assertTrue(isinstance(default_frame, SlideFrame))
        self.assertTrue(isinstance(frame1_frame, SlideFrame))
        self.assertTrue(isinstance(default_frame_parent, SlideFrameParent))
        self.assertTrue(isinstance(frame1_frame_parent, SlideFrameParent))

        # make sure the slide frame is the right size and in the right pos
        self.assertEqual(frame1_frame.size, [200, 100])
        self.assertEqual(frame1_frame.pos, [200, 200])
        self.assertEqual(frame1_frame_parent.size, [400, 300])
        self.assertEqual(frame1_frame_parent.pos, [200, 200])

        # add a widget to the frame
        self.mc.events.post('show_frame_text')
        self.advance_time()

        # make sure the text is in the frame
        self.assertEqual(frame1_frame.current_slide.children[0].text,
                         'TEXT IN FRAME')

        # flip frame to a different slide
        self.mc.events.post('show_frame_text2')
        self.advance_time()

        # make sure the next text is there
        self.assertEqual(frame1_frame.current_slide.children[0].text,
                         'MORE TEXT')

        # flip back to the first frame and make sure that text is there
        self.mc.events.post('show_frame_text')
        self.advance_time()

        self.assertEqual(frame1_frame.current_slide.children[0].text,
                         'TEXT IN FRAME')
