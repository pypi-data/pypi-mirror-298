import os
import zipfile_deflate64 as zipfile
import tempfile
import shutil
from girder import plugin, events, logger
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload
from girder.models.user import User
from girder.exceptions import ValidationException
import traceback
from pathlib import Path

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        events.bind('data.process', 'zip_extractor', self._extract_zip)
        logger.info('ZIP EXTRACTOR: Zip Extractor event bound to data.process')

    def _extract_zip(self, event):
        # print("ZIP EXTRACTOR: _extract_zip method called")
        # print(f"ZIP EXTRACTOR: Event info: {event.info}")

        if 'file' not in event.info:
            logger.error("ZIP EXTRACTOR: No 'file' in event.info")
            return

        print(f"ZIP EXTRACTOR: event: {type(event)=}{event=}\n\n")
        print(f"ZIP EXTRACTOR: event.info: {type(event.info)=}{event.info=}\n\n")
        file = event.info['file']
        
        ## Sanity check
        if 'name' not in file:
            logger.error("ZIP EXTRACTOR: No 'name' attribute in file object")
            return
        logger.info(f"ZIP EXTRACTOR: Processing file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            logger.info(f"ZIP EXTRACTOR: Skipping non-zip file: {file['name']}")
            return
        
        
        try:
            assetstore = File().getAssetstoreAdapter(file)
            file_path = Path(assetstore.fullPath(file))
            logger.info(f"ZIP EXTRACTOR: Zip file path: {file_path}")

            if not file_path.exists():
                logger.error(f"ZIP EXTRACTOR: File not found: {file_path}")
                return

            if 'itemId' in file:
                parent_item = Item().load(file["itemId"], force=True)
                parent_folder = Folder().load(parent_item['folderId'], force=True)
            elif 'folderId' in file:
                parent_folder = Folder().load(file["folderId"], force=True)
            else:
                logger.error("ZIP EXTRACTOR: No 'itemId' or 'folderId' attribute in file object")
                return

            logger.debug(f"ZIP EXTRACTOR: Parent folder: {parent_folder['name']} ({parent_folder['_id']})")

            # Load the user object
            creator = User().load(file["creatorId"], force=True) if 'creatorId' in file else None
            if creator is None:
                logger.error("ZIP EXTRACTOR: Unable to load creator user")
                return

            with tempfile.TemporaryDirectory() as tmpdirname:
                logger.debug(f"ZIP EXTRACTOR: Created temporary directory: {tmpdirname}")
                print(f"Tempdir: {tmpdirname}, type: {type(tmpdirname)}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    logger.debug(f"ZIP EXTRACTOR: Extracted zip contents to: {tmpdirname}")

                tmpdirname = Path(tmpdirname)
                # Remove MAC OS temp directories
                macosx_dir_path =Path(tmpdirname, '__MACOSX')
                if macosx_dir_path.exists():
                    shutil.rmtree(macosx_dir_path, ignore_errors=False)

                # Check if there's a single parent directory
                contents = list(tmpdirname.iterdir())
                logger.debug(f"ZIP EXTRACTOR: Contents of extracted file: {contents}")
                if len(contents) == 1 and Path(tmpdirname, contents[0]).is_dir():
                    tmpdirname = Path(tmpdirname, contents[0])
                    logger.info(f"ZIP EXTRACTOR: Single parent directory detected. New root: {tmpdirname}")

                logger.info(f"ZIP EXTRACTOR: Starting to process extracted files")
                for root, dirs, files in os.walk(tmpdirname):
                    logger.info(f"ZIP EXTRACTOR: Processing directory: {root}")
                    logger.debug(f"ZIP EXTRACTOR: Files in this directory: {files}")
                    for name in files:
                        logger.info(f"ZIP EXTRACTOR: Processing file: {name}")
                        if name.startswith('__MACOSX') or name == '.DS_Store':
                            logger.info(f"ZIP EXTRACTOR: Skipping file: {name}")
                            continue
                        file_path = Path(root, name)
                        relative_path = file_path.relative_to(tmpdirname)
                        logger.info(f"ZIP EXTRACTOR: Processing extracted file: {relative_path}")

                        # Create Girder folder structure
                        current_folder = parent_folder
                        path_parts=os.path.dirname(relative_path).split(os.sep)
                        print(path_parts)
                        # path_parts = relative_path.parent().split(os.sep)
                        logger.debug(f"ZIP EXTRACTOR: current_folder={current_folder}, path_parts={path_parts}")
                        for part in path_parts:
                            if part:
                                try:
                                    new_folder = Folder().createFolder(
                                        parent=current_folder,
                                        name=part,
                                        creator=creator,
                                        reuseExisting=True
                                    )
                                    current_folder = new_folder
                                    logger.debug(f"ZIP EXTRACTOR: Created/found folder: {part} in {current_folder['name']}")
                                except ValidationException as ve:
                                    logger.error(f"ZIP EXTRACTOR: Error creating folder: {part}. Error: {str(ve)}")
                                    raise

                        # Create Girder item and file
                        try:
                            item = Item().createItem(
                                name=relative_path.name,
                                creator=creator,
                                folder=current_folder
                            )
                            logger.debug(f"ZIP EXTRACTOR: Created item: {item['name']} in folder: {current_folder['name']}")

                            with open(file_path, 'rb') as f:
                                uploaded_file = Upload().uploadFromFile(
                                    f, size=os.path.getsize(file_path),
                                    name=relative_path.name,
                                    parentType='item',
                                    parent=item,
                                    user=creator,
                                    # assetstore=assetstore

                                )
                                logger.info(f"ZIP EXTRACTOR: Uploaded file: {uploaded_file['name']} to item: {item['name']}")

                        
                        except ValidationException as ve:
                            logger.error(f"ZIP EXTRACTOR: Error creating item or uploading file: {relative_path}. Error: {str(ve)}")
                            continue

                logger.info(f"ZIP EXTRACTOR: Finished processing all extracted files")

            # Delete the original zip file after extraction
            # FIXME: Does not work
            try:

                print("ZIP EXTRACTOR: Removing item: {file['itemId']}")
                zip_file_item = Item().load(file['itemId'])
                Item.remove(zip_file_item)
                print("ZIP EXTRACTOR: removed")
                # original_file_path = Path(assetstore.fullPath(file))
                # logger.info(f"ZIP EXTRACTOR: Attempting to delete original zip file: {original_file_path}")
                # if original_file_path.exists():
                #     # os.remove(original_file_path)
                #     File().remove(file)
                #     logger.info(f"ZIP EXTRACTOR: Original zip file deleted: {original_file_path}")
                # else:
                #     logger.warning(f"ZIP EXTRACTOR: Original zip file not found: {original_file_path}")
                
                # Remove the file from Girder database
                File().remove(file)
                logger.info(f"ZIP EXTRACTOR: File entry removed from Girder database: {file['name']}")
            except Exception as delete_error:
                logger.error(f"ZIP EXTRACTOR: Error deleting original zip file: {str(delete_error)}")
                logger.error(f"ZIP EXTRACTOR: Delete error traceback: {traceback.format_exc()}")

            logger.info(f"ZIP EXTRACTOR: Zip extraction completed for: {file['name']}")

        except Exception as e:
            logger.error(f"ZIP EXTRACTOR: Error extracting zip file: {file['name']}. Error: {str(e)}")
            logger.error(f"ZIP EXTRACTOR: Traceback: {traceback.format_exc()}")

        logger.info("ZIP EXTRACTOR: Zip extraction process finished")