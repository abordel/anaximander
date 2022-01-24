import os
import subprocess

class Map(object):
    def __init__(self, input_grdobj=None):
        self.grdobj = input_grdobj
        self.operations = []
        self.delta_a = 5
        self.scale = 0

        outfile = os.path.basename(self.grdobj.grdfile)
        base, ext = os.path.splitext(outfile)
        self.outfile = base + '_map' + '.ps'

    def add_coast(self, close=False):
        gmt_cmd = "gmt pscoast "
        gmt_opts = "-R{} -JM7i -B{} -W1/0 -G240 -Df".format(self.grdobj.grdfile, self.delta_a)
        self._run_gmt(gmt_cmd, gmt_opts, close)

    def add_contour(self, close=False):
        gmt_cmd = "gmt grdcontour "
        gmt_opts = "{} -R{} -JM7i -C500 -B{}".format(self.grdobj.grdfile, self.grdobj.grdfile, self.delta_a)
        self._run_gmt(gmt_cmd, gmt_opts, close)

    def add_image(self, close=False, norm=False):
        gmt_cmd = 'gmt grdimage '

        if not norm:
            gmt_opts = '{} -R{} -JM7i -C{} -B{}'.format(self.grdobj.grdfile, self.grdobj.grdfile, self.grdobj.cptfile, self.delta_a)
        else:
            gmt_opts = '{} -I{} -R{} -JM7i -C{} -B{}'.format(self.grdobj.grdfile, self.grdobj.normfile, self.grdobj.grdfile, self.grdobj.cptfile, self.delta_a)

        self._run_gmt(gmt_cmd, gmt_opts, close)

    def add_perspective(self, close=False):
        gmt_cmd = 'gmt grdview '
        gmt_opts = '{} -R{} -JM7i -C{} -Qs -JZ1i -E70/20 -Wc -B{} -I{}'.format(self.grdobj.grdfile, self.grdobj.grdfile, self.grdobj.cptfile, self.delta_a, self.grdobj.normfile)

        self._run_gmt(gmt_cmd, gmt_opts, close)

    def convert(self):
        gmt_cmd = 'gmt psconvert {} -Tg'.format(self.outfile)
        subprocess.run(gmt_cmd.split())

    def _run_gmt(self, command, options, close):
        # if first map command
        if not self.operations:
            if not close:
                cmd_str = command + options + ' -K > ' + self.outfile
            else:
                cmd_str = command + options + ' > ' + self.outfile
        else:
            if close:
                cmd_str = command + options + ' -O >> ' + self.outfile
            else:
                cmd_str = command + options + ' -K >> ' + self.outfile
        subprocess.run(cmd_str.split())
        self.operations.append(cmd_str)


if __name__ == '__main__':
    import grid
    grd = grid.Grid()
    grd.load('etopo1')
    gom_grd = grd.create_subset(['-98','-80','18','32'])
    gom_grd.create_cpt('geo')
    gom_grd.create_illumination()

    m = Map(gom_grd)
    m.add_coast(True)
    #m.add_perspective(close=True)
    m.convert()

    gom_grd.clear()
