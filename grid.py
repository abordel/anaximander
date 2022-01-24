import os
import subprocess


class Grid(object):
    def __init__(self, input_grdfile=None, parent_grdfile=None):
        self.parent_grdfile = parent_grdfile
        self.grdfile = input_grdfile
        self.maskfile = None
        self.cptfile = None
        self.normfile = None
        self.operations = []

    def create_subset(self, region):
        if self.grdfile:
            outgrid = os.path.basename(self.grdfile)
            base, ext = os.path.splitext(outgrid)
            outgrid = base + '_sub' + ext
            gmt_cmd = "gmt grdcut {} -G{} -R{} -Jm0.2".format(self.grdfile, outgrid, '/'.join(region))
            subprocess.run(gmt_cmd.split())
            self.operations.append(gmt_cmd)

            return Grid(outgrid, self.grdfile)

    def create_landmask(self, apply=False):
        if self.grdfile:
            outgrid = os.path.basename(self.grdfile)
            base, ext = os.path.splitext(outgrid)
            outgrid = base + '_lm' + ext
            gmt_cmd = "gmt grdlandmask -G{} -R{}".format(outgrid, self.grdfile)
            subprocess.run(gmt_cmd.split())
            self.operations.append(gmt_cmd)
            self.maskfile=outgrid

            if apply:
                print('apply the landmask')

            return Grid(outgrid, self.grdfile)

    def create_illumination(self):
        """
        Calculate shading
        """
        if self.grdfile:
            outgrid = os.path.basename(self.grdfile)
            base, ext = os.path.splitext(outgrid)

            outgrad = base + '.grad'
            gmt_cmd = "gmt grdgradient {} -A300 -G{} -Nt".format(self.grdfile, outgrad)
            subprocess.run(gmt_cmd.split())
            self.operations.append(gmt_cmd)

            outhist = base + '.hist'
            gmt_cmd = "gmt grdhisteq {} -G{} -N".format(outgrad, outhist)
            subprocess.run(gmt_cmd.split())
            self.operations.append(gmt_cmd)

            outnorm = base + '.norm'
            gmt_cmd = "gmt grdmath {} 4.7 DIV = {}".format(outhist, outnorm)
            subprocess.run(gmt_cmd.split())
            self.operations.append(gmt_cmd)
            self.normfile = outnorm

            os.remove(outgrad)
            os.remove(outhist)

            return Grid(outgrid, self.grdfile)

    def create_cpt(self, color='globe'):
        if self.grdfile:
            outgrid = os.path.basename(self.grdfile)
            base, ext = os.path.splitext(outgrid)
            outcpt = base + '.cpt'
            gmt_cmd = "gmt grd2cpt {} -C{} -Z > {}".format(self.grdfile, color, outcpt)
            subprocess.run(gmt_cmd.split())
            self.cptfile = outcpt
    
    def print_info(self):
        gmt_cmd = "gmt grdinfo {}".format(self.grdfile)
        subprocess.run(gmt_cmd.split())

    def load(self, dataset='etopo1'):
        """
        easily load standard datasets
        """
        data_files = {'etopo1':'etopo1/ETOPO1_Ice_g_gmt4.grd',
                      'gebco':'gebco/GEBCO_2021.nc'}
        data_dir = 'data/'
        self.grdfile = os.path.join(data_dir, data_files[dataset])

    def clear(self):
        """
        delete all files created by this grid object
        """
        if self.maskfile:
            os.remove(self.maskfile)
        if self.cptfile:
            os.remove(self.cptfile)
        if self.normfile:
            os.remove(self.normfile)
