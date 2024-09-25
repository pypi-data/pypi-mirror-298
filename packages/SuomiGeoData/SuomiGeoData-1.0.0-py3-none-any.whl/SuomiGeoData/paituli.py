import os
import io
import zipfile
import typing
import geopandas
import requests
import tempfile
from .core import Core
from .syke import Syke


class Paituli:

    '''
    Executes downloading and extracting data from Paituli
    (https://paituli.csc.fi/download.html).
    '''

    @property
    def indexmap_dem(
        self
    ) -> geopandas.GeoDataFrame:

        '''
        Returns a GeoDataFrame containing the DEM index map.
        '''

        output = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'nls_dem_index.shp'
            )
        )

        return output

    @property
    def indexmap_tdb(
        self
    ) -> geopandas.GeoDataFrame:

        '''
        Returns a GeoDataFrame containing the topographic database index map.
        '''

        output = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'nls_td_index.shp'
            )
        )

        return output

    def save_indexmap_dem(
        self,
        file_path: str,
        **kwargs: typing.Any
    ) -> str:

        '''
        Saves the GeoDataFrame of the DEM index map to the specified file path
        and return a success message.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` method.

        Returns
        -------
        str
            A confirmation message indicating the output file has been saved.
        '''

        check_file = Core().is_valid_ogr_driver(file_path)
        if check_file is True:
            self.indexmap_dem.to_file(
                file_path,
                **kwargs
            )
        else:
            raise Exception(
                'Could not retrieve driver from the file path.'
            )

        return 'GeoDataFrame saved to the output file.'

    def save_indexmap_tdb(
        self,
        file_path: str,
        **kwargs: typing.Any
    ) -> str:

        '''
        Saves the GeoDataFrame of the topographic database
        index map to the specified file path and returns a success message.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` method.

        Returns
        -------
        str
            A confirmation message indicating the output file has been saved.
        '''

        check_file = Core().is_valid_ogr_driver(file_path)
        if check_file is True:
            self.indexmap_tdb.to_file(
                file_path,
                **kwargs
            )
        else:
            raise Exception(
                'Could not retrieve driver from the file path.'
            )

        return 'GeoDataFrame saved to the output file.'

    @property
    def dem_labels(
        self
    ) -> list[str]:

        '''
        Returns the list of labels from the DEM index map.
        '''

        output = list(self.indexmap_dem['label'])

        return output

    @property
    def tdb_labels(
        self
    ) -> list[str]:

        '''
        Returns the list of labels from the topographic database index map.
        '''

        output = list(self.indexmap_tdb['label'])

        return output

    def is_valid_label_dem(
        self,
        label: str
    ) -> bool:

        '''
        Returns whether the label exists in the DEM index map.

        Parameters
        ----------
        label : str
            Name of the label.

        Returns
        -------
        bool
            True if the label exists, False otherwise.
        '''

        return label in self.dem_labels

    def is_valid_label_tdb(
        self,
        label: str
    ) -> bool:

        '''
        Returns whether the label exists in the topographic database index map.

        Parameters
        ----------
        label : str
            Name of the label.

        Returns
        -------
        bool
            True if the label exists, False otherwise.
        '''

        return label in self.tdb_labels

    def dem_download_by_labels(
        self,
        labels: list[str],
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads the DEM raster files for the given labels and
        returns a confirmation message.

        Parameters
        ----------
        labels : list of str
            List of label names from the DEM index map.

        folder_path : str
            Path of empty folder to save the downloaded raster files.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that all downloads are complete.
        '''

        # check the existence of the output folder path
        if os.path.isdir(folder_path):
            exist_files = len(os.listdir(folder_path))
            if exist_files > 0:
                raise Exception(
                    'Output folder must be empty.'
                )
            else:
                pass
        else:
            raise Exception(
                'The folder path does not exist.'
            )

        # check whether the input labels exist
        for label in labels:
            if self.is_valid_label_dem(label):
                pass
            else:
                raise Exception(
                    f'The label {label} does not exist in the index map.'
                )

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download topographic database
        suffix_urls = self.indexmap_dem[self.indexmap_dem['label'].isin(labels)]['path']
        count = 1
        for label, url in zip(labels, suffix_urls):
            label_url = Core()._url_prefix_paituli_dem_tdb + url
            response = requests.get(
                url=label_url,
                headers=headers
            )
            downloaded_file = os.path.join(
                folder_path, f'{label}.tif'
            )
            with open(downloaded_file, 'wb') as downloaded_raster:
                downloaded_raster.write(response.content)
            print(
                f'Download of label {label} completed (count {count}/{len(labels)}).'
            )
            count = count + 1

        return 'All downloads are complete.'

    def tdb_download_by_labels(
        self,
        labels: list[str],
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads the topographic database folders of shapefiles for the given labels and
        returns a confirmation message.

        Parameters
        ----------
        labels : list of str
            List of label names from the topographic database index map.

        folder_path : str
            Path of empty folder to save the downloaded folder of shapefiles.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that all downloads are complete.
        '''

        # check whether the input labels exist
        for label in labels:
            if self.is_valid_label_tdb(label):
                pass
            else:
                raise Exception(
                    f'The label {label} does not exist in the index map.'
                )

        # check the existence of the given folder path
        if os.path.isdir(folder_path):
            exist_files = len(os.listdir(folder_path))
            if exist_files > 0:
                raise Exception(
                    'Output folder must be empty.'
                )
            else:
                pass
        else:
            raise Exception(
                'The folder path does not exist.'
            )

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download topographic database
        suffix_urls = self.indexmap_tdb[self.indexmap_tdb['label'].isin(labels)]['path']
        count = 1
        for label, url in zip(labels, suffix_urls):
            label_url = Core()._url_prefix_paituli_dem_tdb + url
            response = requests.get(
                url=label_url,
                headers=headers
            )
            downloaded_data = io.BytesIO(response.content)
            with zipfile.ZipFile(downloaded_data, 'r') as downloaded_zip:
                downloaded_zip.extractall(
                    os.path.join(folder_path, label)
                )
            print(
                f'Download of label {label} completed (count {count}/{len(labels)}).'
            )
            count = count + 1

        return 'All downloads are complete.'

    @property
    def get_example_area(
        self
    ) -> geopandas.GeoDataFrame:

        '''
        Returns a GeoDataFrame of example area to test
        raster and vector downloads.
        '''

        output = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'example_area.shp'
            )
        )

        return output

    def dem_labels_download_by_area(
        self,
        input_area: str | geopandas.GeoDataFrame,
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads the DEM raster files for the given labels and
        returns a confirmation message.

        Parameters
        ----------
        input_area : str or GeoDataFrame
            Input area by either file path or GeoDataFrame.

        folder_path : str
            Path of empty folder to save the downloaded raster files.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that all downloads are complete.
        '''

        # input area
        if isinstance(input_area, str):
            area_gdf = geopandas.read_file(input_area)
        elif isinstance(input_area, geopandas.GeoDataFrame):
            area_gdf = input_area
        else:
            raise Exception('Input area must be either file or GeoDataFrame format.')

        # check crs of input area
        target_crs = 'EPSG:3067'
        if area_gdf.crs is None:
            area_gdf = area_gdf.set_crs(target_crs)
        elif str(area_gdf.crs) != target_crs:
            area_gdf = area_gdf.to_crs(target_crs)
        else:
            pass

        # DEM index map
        index_gdf = self.indexmap_dem

        # labels
        label_gdf = geopandas.sjoin(index_gdf, area_gdf, how='inner').reset_index(drop=True)
        label_gdf = label_gdf.drop_duplicates(subset=['label']).reset_index(drop=True)

        # download labels
        if label_gdf.shape[0] == 0:
            raise Exception('The index map does not intersect with the given area.')
        else:
            message = self.dem_download_by_labels(
                labels=list(label_gdf['label']),
                folder_path=folder_path,
                http_headers=http_headers
            )

        return message

    def dem_labels_download_by_syke_subcatchment(
        self,
        input_file: str,
        level: int,
        single_area: int,
        folder_path: str,
        merge_polygons: bool = True,
        percentage_cutoff: float = 0,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads the DEM raster files for the given subcatchment division of Syke and
        returns a confirmation message.

        Parameters
        ----------
        input_file : str
            Path to the shapefile of catchment area divisions, obtained from the
            :meth: `SuomiGeoData.Syke.download_catchment_divisions_2023` method.

        level : int
            Level of catchment division and must be one of 1, 2, 3, 4 or 5.

        single_area : int
            Selected value from 'taso<level>_osai' columns.

        folder_path : str
            Path of empty folder path to save the downloaded raster files.

        merge_polygons : bool, optional
            Merges the polygons using the :meth:`geopandas.GeoDataFrame.dissolve` method
            and explodes them with the :meth:`geopandas.GeoDataFrame.explode` method. If False,
            no operation is performed.

        percentage_cutoff : float, optional
            Excludes polygon below the specified area percentage, ranging from 0 to 100,
            relative to the total area of all polygons. Default is 0, excluding negligible polygons.
            Provide -1 for no exclusion.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that all downloads are complete.
        '''

        # input area
        area_gdf = Syke().select_single_subcatchment(
            input_file=input_file,
            level=level,
            single_area=single_area,
            merge_polygons=merge_polygons,
            percentage_cutoff=percentage_cutoff
        )

        # DEM index map
        index_gdf = self.indexmap_dem

        # labels
        label_gdf = geopandas.sjoin(index_gdf, area_gdf, how='inner').reset_index(drop=True)
        label_gdf = label_gdf.drop_duplicates(subset=['label']).reset_index(drop=True)

        # download labels
        message = self.dem_download_by_labels(
            labels=list(label_gdf['label']),
            folder_path=folder_path,
            http_headers=http_headers
        )

        return message

    def dem_clipped_download_by_area(
        self,
        input_area: str | geopandas.GeoDataFrame,
        output_file: str,
        http_headers: typing.Optional[dict[str, str]] = None,
        **kwargs: typing.Any
    ) -> str:

        '''
        Downloads the clipped DEM raster file for the given area and
        returns a confirmation message.

        Parameters
        ----------
        input_area : str or GeoDataFrame
            Input area by either file path or GeoDataFrame.

        folder_path : str
            Path of empty folder to save the downloaded raster files.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        **kwargs : optional
            Additional keyword arguments for updating the dictionary of
            :attr:`rasterio.profile` attribute.

        Returns
        -------
        str
            A confirmation message indicating that all geoprocesssings are complete.
        '''

        with tempfile.TemporaryDirectory() as tmp_dir:
            message = self.dem_labels_download_by_area(
                input_area=input_area,
                folder_path=tmp_dir,
                http_headers=http_headers
            )
            print(message)
            # merging rasters
            message = Core().raster_merging(
                folder_path=tmp_dir,
                output_file=os.path.join(tmp_dir, 'merged.tif'),
                compress='lzw'
            )
            print(message)
            # clipping rasters
            message = Core().raster_clipping_by_mask(
                input_file=os.path.join(tmp_dir, 'merged.tif'),
                mask_area=input_area,
                output_file=output_file,
                **kwargs
            )
            print(message)

        return 'All geoprocessing has been completed.'

    def dem_clipped_download_by_syke_subcatchment(
        self,
        input_file: str,
        level: int,
        single_area: int,
        output_file: str,
        merge_polygons: bool = True,
        percentage_cutoff: float = 0,
        http_headers: typing.Optional[dict[str, str]] = None,
        **kwargs: typing.Any
    ) -> str:

        '''
        Downloads the clipped DEM raster file for the given subcatchment division of Syke and
        returns a confirmation message.

        Parameters
        ----------
        input_file : str
            Path to the shapefile of catchment area divisions, obtained from the
            :meth: `SuomiGeoData.Syke.download_catchment_divisions_2023` method.

        level : int
            Level of catchment division and must be one of 1, 2, 3, 4 or 5.

        single_area : int
            Selected value from 'taso<level>_osai' columns.

        output_file : str
            File path to save the output raster.

        merge_polygons : bool, optional
            Merges the polygons using the :meth:`geopandas.GeoDataFrame.dissolve` method
            and explodes them with the :meth:`geopandas.GeoDataFrame.explode` method. If False,
            no operation is performed.

        percentage_cutoff : float, optional
            Excludes polygon below the specified area percentage, ranging from 0 to 100,
            relative to the total area of all polygons. Default is 0, excluding negligible polygons.
            Provide -1 for no exclusion.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        **kwargs : optional
            Additional keyword arguments for updating the dictionary of
            :attr:`rasterio.profile` attribute.

        Returns
        -------
        str
            A confirmation message indicating that all geoprocessing are complete.
        '''

        # input subcatchment
        area_gdf = Syke().select_single_subcatchment(
            input_file=input_file,
            level=level,
            single_area=single_area,
            merge_polygons=merge_polygons,
            percentage_cutoff=percentage_cutoff
        )

        # DEM index map
        index_gdf = self.indexmap_dem

        # labels
        label_gdf = geopandas.sjoin(index_gdf, area_gdf, how='inner').reset_index(drop=True)
        label_gdf = label_gdf.drop_duplicates(subset=['label']).reset_index(drop=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            # download labels
            message = self.dem_download_by_labels(
                labels=list(label_gdf['label']),
                folder_path=tmp_dir,
                http_headers=http_headers
            )
            print(message)
            # merging rasters
            message = Core().raster_merging(
                folder_path=tmp_dir,
                output_file=os.path.join(tmp_dir, 'merged.tif'),
                compress='lzw'
            )
            print(message)
            # clipping rasters
            message = Core().raster_clipping_by_mask(
                input_file=os.path.join(tmp_dir, 'merged.tif'),
                mask_area=area_gdf,
                output_file=output_file,
                **kwargs
            )
            print(message)

        return 'All geoprocessing has been completed.'
