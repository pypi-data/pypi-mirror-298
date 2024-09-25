#=======================================================================
"""
Decode FLV file
"""
#       References:
#       https://en.wikipedia.org/wiki/Flash_Video
#       https://www.adobe.com/content/dam/acom/en/devnet/flv/video_file_format_spec_v10.pdf
#=======================================================================
from .decoder import Decoder
from .hexdumper import HexDumper

class FLVDecoder(Decoder):
    def __init__(self, file, view):
        super(FLVDecoder,self).__init__(file, view, big_endian=True)

    def run(self):
        # FLV header
        sig = self.read(3)
        if sig != b'FLV':
            raise ValueError('Not a FLV file')
        self.vset('Version', self.u1())
        tf = self.u1()
        assert (tf & 0b11111010) == 0
        self.vset('AudioTags', (tf & 4) != 0)
        self.vset('VideoTags', (tf & 1) != 0)
        doff = self.u4()
        self.vset('DataOffset', doff)
        self.read(doff - self.pos)
        with self.view.array('Tag'):
            i = 0
            while True:
                with self.view.map(i):
                    # Sequence of back-pointers
                    self.vset('PreviousTagSize', self.u4())
                    self.tag()
                    #break
                i += 1

    def tag(self):
        tagtype = self.u1()
        if tagtype == 8:
            self.vset('TagType', 'audio')
        elif tagtype == 9:
            self.vset('TagType', 'video')
        elif tagtype == 18:
            self.vset('TagType', 'script data')
        else:
            self.vset('TagType', tagtype)
        dsize = self.ui24()
        self.vset('DataSize', dsize)
        self.vset('Timestamp', self.ui24())
        self.vset('TimestampExtended', self.u1())
        self.vset('StreamID', self.ui24())
        with self.substream(dsize):
            if tagtype == 18:
                self.script_data()
            elif tagtype == 9:
                self.video_data()
            self.hexdump(self.read())

    frametype_map = {1:'keyframe',
                     2:'inter frame',
                     3:'disposable inter frame',
                     4:'generated keyframe',
                     5:'video info/command frame'}
    codecid_map = {1:'JPEG',
                   2:'Sorenson H.263',
                   3:'Screen video',
                   4:'On2 VP6',
                   5:'On2 VP6 with alpha channel',
                   6:'Screen video version 2',
                   7:'AVC'}

    def video_data(self):
        with self.view.map('VideoData'):
            tid = self.u1()
            ftype = tid >> 4
            codecid = tid & 0xf
            self.vset('FrameType', self.frametype_map.get(ftype,ftype))
            self.vset('CodecID', self.codecid_map.get(codecid,codecid))
            
    def script_data(self):
        with self.view.array('ScriptData'):
            i = 0
            while True:
                nt = self.u1()
                if nt == 0:
                    endval = self.u2()
                    assert endval == 9
                    break
                if nt != 2:
                    raise ValueError('Expected 2 SCRIPTDATANAME')
                nlen = self.u2()
                name = self.read(nlen).decode('ascii')
                with self.view.map(i):
                    if nt not in (2, 12):
                        raise ValueError('Unexpected type %d for name' % nt)
                    self.vset('Name', name)
                    vt, value = self.obj()
                    if vt == 8: # ECMAarray
                        alen = value
                        with self.view.map('Value'):
                            for i in range(alen):
                                klen = self.u2()
                                key = self.read(klen).decode('ascii')
                                xt, xvalue = self.obj()
                                self.vset(key, xvalue)
                    else:
                        self.vset('Value', value)
                #nlen = self.u2()
                #if nlen == 0:
                #    # 00 00 09 = SCRIPTDATAOBJECTEND

    def obj(self):
        otype = self.u1()
        if otype == 0:          # Number
            value = self.f8()
            if value == int(value):
                value = int(value)
        elif otype == 1:        # Boolean
            value = self.u1()
        elif otype == 2:        # String
            nlen = self.u2()
            value = self.read(nlen).decode('ascii')
        elif otype == 8:        # ECMA array
            value = self.u4()   # Length
        else:
            raise NotImplementedError('Value type %d' % otype)
        return otype, value

    # Output methods
    def hexdump(self, data, limit=256):
        for line in HexDumper(data[:limit]).iter_lines():
            offset, _, dump = line.partition(': ')
            self.vset(offset[1:].replace(' ','0'), dump)
        if len(data) > limit:
            self.vset('dump_size', len(data))
                      
    # FLV-specific low-level items
    def ui24(self):
        hi = self.u1()
        lo = self.u2()
        return (hi << 16) | lo

    def s4(self):
        """Read a 4-byte string (fourcc)"""
        b4 = self.read(4)
        return b4.decode('iso-8859-1')

def main():
    from .viewer import PlainViewer
    import sys
    view = PlainViewer()
    with open(sys.argv[1],'rb') as f:
        dec = FLVDecoder(f, view)
        dec.run()

if __name__=='__main__':
    main()
