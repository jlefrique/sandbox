#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time
import sys
import serial
import datetime

# on which port should the tests be performed:
PORT = 'loop://'

STEP_NB = 10000


loopback_payload = bytes(bytearray(range(33, 127)))


def segments(data, size=16):
    for a in range(0, len(data), size):
        yield data[a:a + size]


class TestCpuScalingEffect(unittest.TestCase):
    """Test with timeouts"""
    timeout = 0

    def setUp(self):
        self.s = serial.serial_for_url(PORT, baudrate=3000000, timeout=self.timeout)

    def tearDown(self):
        self.s.close()

    @unittest.skip('skip')
    def test01_delay(self):

        max_duration = 0
        min_duration = float('inf')

        n = 0
        while n < STEP_NB:
            n += 1

            start_time = datetime.datetime.now()
            time.sleep(0.02)
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            print("Duration: {} us".format(duration.microseconds))

            if duration.microseconds > max_duration:
                max_duration = duration.microseconds
            if duration.microseconds < min_duration:
                min_duration = duration.microseconds

            self.assertAlmostEqual(duration.microseconds, 20000, delta=2000)

        print("Duration: [{}, {}] us".format(min_duration, max_duration))

    def test10_serial_read_empty(self):
        """timeout: After port open, the input buffer must be empty"""
        self.assertEqual(self.s.read(1), b'', "expected empty buffer")

    # @unittest.skip('skip')
    def test11_serial_loopback(self):
        """timeout: each sent character should return (binary test).
        this is also a test for the binary capability of a port."""
        max_duration = 0
        n = 0

        while n < STEP_NB:
            print("Step {}".format(n))
            n += 1

            for block in segments(loopback_payload, 128):

                length = len(block)
                print("===> {}".format(block))
                start_time = datetime.datetime.now()

                self.s.write(block)
                # there might be a small delay until the character is ready (especially on win32)
                #time.sleep(0.005)

                self.assertEqual(
                    self.s.in_waiting, length,
                    "expected exactly {} character for inWainting()".format(length))

                readback = self.s.read(length)
                print("<=== {}".format(readback))
                self.assertEqual(readback, block)

                self.assertEqual(
                    self.s.read(1), b'',
                    "expected empty buffer after all sent chars are read")

                end_time = datetime.datetime.now()
                duration = end_time - start_time
                print("Duration: {} us".format(duration.microseconds))
                if duration.microseconds > max_duration:
                    max_duration = duration.microseconds

                #self.assertAlmostEqual(duration.microseconds, 1000, delta=1000)

        print("Max duration: {} us".format(max_duration))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    sys.stdout.write("Testing port: {!r}\n".format(PORT))
    sys.argv[1:] = ['-v']
    unittest.main()
