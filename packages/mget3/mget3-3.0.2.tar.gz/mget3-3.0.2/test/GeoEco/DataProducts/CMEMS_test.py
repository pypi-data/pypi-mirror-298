# CMEMS_test.py - pytest tests for GeoEco.DataProducts.CMEMS.
#
# Copyright (C) 2024 Jason J. Roberts
#
# This file is part of Marine Geospatial Ecology Tools (MGET) and is released
# under the terms of the 3-Clause BSD License. See the LICENSE file at the
# root of this project or https://opensource.org/license/bsd-3-clause for the
# full license text.

import datetime
import logging
import os
from pathlib import Path

import numpy
import pytest

from GeoEco.Logging import Logger
from GeoEco.DataProducts.CMEMS import CMEMSARCOArray
from GeoEco.Datasets.GDAL import GDALDataset

Logger.Initialize()


def getCMEMSCredentials():
    try:
        import dotenv
        dotenv.load_dotenv(Path(__file__).parent.parent.parent / '.env')
        return (os.getenv('CMEMS_USERNAME'), os.getenv('CMEMS_PASSWORD'))
    except:
        return None, None


def isArcPyInstalled():
    try:
        import arcpy
    except:
        return False
    return True


@pytest.mark.skipif(None in getCMEMSCredentials(), reason='CMEMS_USERNAME or CMEMS_PASSWORD environment variables not defined')
@pytest.mark.skipif(not isArcPyInstalled(), reason='ArcGIS arcpy module is not installed')
class TestCMEMSARCOArrayArcGIS():

    # Test that we can download arrays of all supported dimensions. Note: I
    # could not find dataset with zyx dimensions, e.g. a cumulative
    # climatology of something that has depth layers. So this case is not
    # tested.

    def test_CreateArcGISRasters_yx(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_glo_phy_my_0.083deg_static'
        vsn = 'mdt'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir)
        assert (outputDir / datasetID / ('%s.img' % vsn)).is_file()

    def test_CreateArcGISRasters_tyx_monthly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           spatialExtent='-82 25 -52 50',
                                           startDate=datetime.datetime(2020,1,1),
                                           endDate=datetime.datetime(2020,3,31))
        for month in [1,2,3]:
            assert (outputDir / datasetID / vsn / ('%s_2020%02i.img' % (vsn, month))).is_file()

    def test_CreateArcGISRasters_tzyx_monthly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_glo_phy_my_0.083deg_P1M-m'
        vsn = 'thetao'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           spatialExtent='-82 25 -52 50',
                                           minDepth=0.,
                                           maxDepth=5.,
                                           startDate=datetime.datetime(2020,1,1),
                                           endDate=datetime.datetime(2020,3,31))
        for depth in ['0000.5', '0001.5', '0002.6', '0003.8']:
            for month in [1,2,3]:
                assert (outputDir / datasetID / vsn / ('Depth_' + depth) / ('%s_%s_2020%02i.img' % (vsn, depth, month))).is_file()

    # Test that products with temporal resolutions other than monthly (which we
    # tested above) are created with appropriate file names.

    def test_CreateArcGISRasters_tzyx_daily(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_glo_phy_my_0.083deg_P1D-m'
        vsn = 'thetao'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           spatialExtent='-82 25 -52 50',
                                           minDepth=0.,
                                           maxDepth=5.,
                                           startDate=datetime.datetime(2020,1,1,0,0,0),
                                           endDate=datetime.datetime(2020,1,3,23,59,59))
        for depth in ['0000.5', '0001.5', '0002.6', '0003.8']:
            for day in [1,2,3]:
                assert (outputDir / datasetID / vsn / ('Depth_' + depth) / '2020' / ('%s_%s_202001%02i.img' % (vsn, depth, day))).is_file()

    def test_CreateArcGISRasters_tyx_hourly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_blk_phy-ssh_anfc_2.5km_PT1H-m'
        vsn = 'zos'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           startDate=datetime.datetime(2024,1,1,0,0,0),
                                           endDate=datetime.datetime(2024,1,1,23,59,59))
        for hour in range(24):
            assert (outputDir / datasetID / vsn / '2024' / ('%s_20240101_%02i0000.img' % (vsn, hour))).is_file()

    def test_CreateArcGISRasters_tyx_15min(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_blk_phy-ssh_anfc_2.5km_PT15M-i'
        vsn = 'zos'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           startDate=datetime.datetime(2024,1,1,0,0,0),
                                           endDate=datetime.datetime(2024,1,1,2,59,59))
        for hour in range(3):
            for minute in [0, 15, 30, 45]:
                assert (outputDir / datasetID / vsn / '2024' / ('%s_20240101_%02i%02i00.img' % (vsn, hour, minute))).is_file()

    # Test creation of seafloor grids.

    def test_CreateArcGISRasters_tzyx_monthly_seafloor(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_glo_phy_my_0.083deg_P1M-m'
        vsn = 'thetao'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           spatialExtent='-82 25 -52 50',
                                           minDepth=20000.,
                                           startDate=datetime.datetime(2020,1,1),
                                           endDate=datetime.datetime(2020,2,28))
        for month in [1,2]:
            assert (outputDir / datasetID / vsn / 'Depth_20000.0' / ('%s_20000.0_2020%02i.img' % (vsn, month))).is_file()

    # Test log10 transform.

    def test_log10_transform(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M'
        vsn = 'CHL'
        outputDir = tmp_path / vsn
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           spatialExtent='-82 25 -52 50',
                                           startDate=datetime.datetime(2020,1,1),
                                           endDate=datetime.datetime(2020,3,31))
        normalData = []
        for month in [1,2,3]:
            normalData.append(GDALDataset.GetRasterBand(outputDir / datasetID / vsn / ('%s_2020%02i.img' % (vsn, month))))

        outputDir = tmp_path / (vsn + '_log10' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           log10Transform=True,
                                           spatialExtent='-82 25 -52 50',
                                           startDate=datetime.datetime(2020,1,1),
                                           endDate=datetime.datetime(2020,3,31))
        log10Data = []
        for month in [1,2,3]:
            log10Data.append(GDALDataset.GetRasterBand(outputDir / datasetID / vsn / ('%s_2020%02i.img' % (vsn, month))))

        for i in range(len(normalData)):
            hasData = numpy.invert(normalData[i].numpy_equal_nan(normalData[i].Data[:], normalData[i].NoDataValue))
            assert (numpy.log10(normalData[i].Data[:][hasData]) == log10Data[i].Data[:][hasData]).all()

    def test_log10_transform_warning(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_mod_glo_phy_my_0.083deg_P1D-m'
        vsn = 'thetao'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateArcGISRasters(username=username,
                                           password=password,
                                           datasetID=datasetID,
                                           variableShortName=vsn,
                                           outputWorkspace=outputDir,
                                           log10Transform=True,
                                           spatialExtent='-82 25 -52 50',
                                           minDepth=0.,
                                           maxDepth=1.,
                                           startDate=datetime.datetime(2020,1,1,0,0,0),
                                           endDate=datetime.datetime(2020,1,3,23,59,59))
        # I could not figure out how to capture the warning via caplog or
        # capsys. But I did verify it was printed by examining the logging
        # output.

    # Test climatologies.

    def test_CreateClimatologicalArcGISRasters_tyx_monthly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        for statistic in ['Count', 'Maximum', 'Mean', 'Minimum', 'Range', 'Standard Deviation', 'Sum']:
            CMEMSARCOArray.CreateClimatologicalArcGISRasters(username=username,
                                                             password=password,
                                                             datasetID=datasetID,
                                                             variableShortName=vsn,
                                                             statistic=statistic,
                                                             binType='Monthly',
                                                             outputWorkspace=outputDir,
                                                             spatialExtent='-82 25 -52 50',
                                                             startDate=datetime.datetime(2020,1,1),
                                                             endDate=datetime.datetime(2021,12,31))
            for month in range(1,13):
                assert (outputDir / datasetID / vsn / 'Monthly_Climatology' / ('%s_month%02i_%s.img' % (vsn, month, statistic.lower()))).is_file()

    def test_CreateClimatologicalArcGISRasters_tyx_cumulative(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateClimatologicalArcGISRasters(username=username,
                                                         password=password,
                                                         datasetID=datasetID,
                                                         variableShortName=vsn,
                                                         statistic='Mean',
                                                         binType='Cumulative',
                                                         outputWorkspace=outputDir,
                                                         spatialExtent='-82 25 -52 50',
                                                         startDate=datetime.datetime(2020,1,1),
                                                         endDate=datetime.datetime(2021,12,31))
        assert (outputDir / datasetID / vsn / 'Cumulative_Climatology' / ('%s_cumulative_mean.img' % vsn)).is_file()

    def test_CreateClimatologicalArcGISRasters_tyx_seasonal(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateClimatologicalArcGISRasters(username=username,
                                                         password=password,
                                                         datasetID=datasetID,
                                                         variableShortName=vsn,
                                                         statistic='Mean',
                                                         binType='Monthly',
                                                         binDuration=3,
                                                         outputWorkspace=outputDir,
                                                         spatialExtent='-82 25 -52 50',
                                                         startDate=datetime.datetime(2020,1,1),
                                                         endDate=datetime.datetime(2021,12,31))
        for month in [1,4,7,10]:
            assert (outputDir / datasetID / vsn / '3month_Climatology' / ('%s_months%02ito%02i_mean.img' % (vsn, month, month + 2))).is_file()

    def test_CreateClimatologicalArcGISRasters_tyx_daily(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CreateClimatologicalArcGISRasters(username=username,
                                                         password=password,
                                                         datasetID=datasetID,
                                                         variableShortName=vsn,
                                                         statistic='Mean',
                                                         binType='Daily',
                                                         binDuration=8,
                                                         outputWorkspace=outputDir,
                                                         spatialExtent='-82 25 -52 50',
                                                         startDate=datetime.datetime(2020,1,1),
                                                         endDate=datetime.datetime(2021,12,31))
        for day in range(1, 366, 8):
            assert (outputDir / datasetID / vsn / '8day_Climatology' / ('%s_days%03ito%03i_mean.img' % (vsn, day, min(day + 7, 366)))).is_file()

    # Test Canny fronts.

    def test_CannyEdgesAsArcGISRasters_tyx_monthly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CannyEdgesAsArcGISRasters(username=username,
                                                 password=password,
                                                 datasetID=datasetID,
                                                 variableShortName=vsn,
                                                 outputWorkspace=outputDir,
                                                 spatialExtent='-82 25 -52 50',
                                                 startDate=datetime.datetime(2020,1,1),
                                                 endDate=datetime.datetime(2020,1,10))
        for day in range(1, 10):
            assert (outputDir / datasetID / (vsn + '_fronts') / '2020' / ('%s_fronts_202001%02i.img' % (vsn, day))).is_file()

    def test_log10_CannyEdgesAsArcGISRasters_tyx_monthly(self, tmp_path):
        username, password = getCMEMSCredentials()
        datasetID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D'
        vsn = 'CHL'
        outputDir = tmp_path / (vsn + '1' )
        os.makedirs(outputDir)
        CMEMSARCOArray.CannyEdgesAsArcGISRasters(username=username,
                                                 password=password,
                                                 datasetID=datasetID,
                                                 variableShortName=vsn,
                                                 outputWorkspace=outputDir,
                                                 log10Transform=True,
                                                 spatialExtent='-82 25 -52 50',
                                                 startDate=datetime.datetime(2020,1,1),
                                                 endDate=datetime.datetime(2020,1,10))
        for day in range(1, 10):
            assert (outputDir / datasetID / (vsn + '_fronts') / '2020' / ('%s_fronts_202001%02i.img' % (vsn, day))).is_file()
