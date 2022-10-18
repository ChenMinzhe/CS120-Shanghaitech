import rec_and_play
import numpy
from rec_and_play import SAMPLE_RATE

t=numpy.arange(0, 20*SAMPLE_RATE)

out = (numpy.sin(2 * numpy.pi * 698 * (t/SAMPLE_RATE)) + numpy.sin(2 * numpy.pi * 987 * (t/SAMPLE_RATE)) + numpy.sin(2 * numpy.pi * 1244 * (t/SAMPLE_RATE))) * 16383
out_bytestream = out.astype(numpy.short).tostring()

rec_and_play.play_bytestream(out_bytestream)
