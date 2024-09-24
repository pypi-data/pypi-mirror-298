import inspect
import syft as sy
from syft.types.uid import UID
from syft.service.user.user import ServiceRole

class Data3Network:
    """
    :Description: Data3Network class provides methods to interact with the PySyft Server
    :Method login: Login to the PySyft Server
    :Method set_admin_credential: Set the admin credentials
    :Method register_user: Register a new user
    :Method remove_user: Remove a user
    :Method view_users: View all users
    :Method create_contributor: Create a contributor
    :Method create_asset: Create an asset
    :Method create_dataset: Create a dataset
    :Method upload_dataset: Upload a dataset
    :Method view_dataset: View a dataset
    :Method view_datasets: View all datasets
    :Method view_assets: View all assets in a dataset
    :Method remove_dataset: Remove a dataset
    """
    
    #*******************************#
    #*     Admin User methods      *#
    #*******************************#

    def login(self, ip: str, default_email: str, default_password: str):
        """
        :Description: Login to the PySyft Server
        :Param ip: IP address of the PySyft Server
        :Param default_email: Default email address of the user
        :Param default_password: Default password of the user
        :Return: PySyft Client object
        """
        try:
            client = sy.login(url=ip, email=default_email, password=default_password)       
            return client
        except Exception as e:
            raise Exception(f"{e}")

    def set_admin_credential(self,client, name:str| None, new_email: str | None = None, new_password: str | None = None):
        """
        :Description: Set the admin credentials
        :Param client: PySyft Client object
        :Param name: Name of the user
        :Param new_email: New email address of the user
        :Param new_password: New password of the user
        :Return: True if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")
            if name is not None and name != "":
                client.account.update(name=name)       
            
            if self._user_exists(client,new_email):
                self.remove_user(new_email, client)
                self.register_user(client,"ADMIN", name, new_email, new_password)
                return True
                    
        except Exception as e:
            raise Exception(f"{e}")
        
    def register_user(self, client, user_role, user_name, user_email, user_password):
        """
        :Description: Register a new user
        :Param client: PySyft Client object
        :Param user_role: Role of the user
        :Param user_name: Name of the user
        :Param user_email: Email address of the user
        :Param user_password: Password of the user
        :Return: True if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")

            if str(user_role).upper() not in  ["ADMIN", "GUEST", "DATA_SCIENTIST"]:
                raise Exception("Invalid user role.")

            client.users.create(
                email=user_email,
                name=user_name,
                password=user_password,
                password_verify=user_password,
                role=str(user_role).upper()
            )
            
            return True
        except Exception as e:
            raise Exception(f"{e}")
            

    def remove_user(self, email: str, client):
        """
        :Description: Remove a user
        :Param email: Email address of the user
        :Param client: PySyft Client object
        :Return: True if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")
            users = client.users.get_all()

            user = next((user for user in users if user.email == email), None)
            if user is None:
                raise Exception(f"User with email {email} not found.")    
            
            user_uid = UID(user.id)
            client.users.delete(user_uid)
            
            return True
        except Exception as e:
            raise Exception(f"{e}")

    def view_users(self, client):
        """
        :Description: View all users
        :Param client: PySyft Client object
        :Return: List of users if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")
            users = client.users.get_all()
            return users
        except Exception as e:
            raise Exception(f"{e}")
        

    #*******************************#
    #*       Dataset methods       *#
    #*******************************#

    def create_contributor(self, name: str, role: str, email: str):
        """
        :Description: Create a contributor
        :Param name: Name of the contributor
        :Param role: Role of the contributor
        :Param email: Email address of the contributor
        :Return: Contributor object if successful else raise exception
        """
        try:
            contributor = sy.Contributor(name=name, role=role, email=email)  
            return contributor
        except Exception as e:
            raise Exception(f"{e}")
    
    def create_asset(self,name:str, description:str, data, mock, contributors: list):
        """
        :Description: Create an asset
        :Param name: Name of the asset
        :Param description: Description of the asset
        :Param data: Data of the asset
        :Param mock: Mock data of the asset
        :Param contributors: List of contributors
        :Return: Asset object if successful else raise exception
        """
        try:
            asset = sy.Asset(name=name, description=description, data=data, mock=mock, contributors=contributors)
            return asset
        except Exception as e:
            raise Exception(f"{e}")        
    
    def create_dataset(self, name: str, description: str, assets: list, contributors: list):
        """
        :Description: Create a dataset
        :Param name: Name of the dataset
        :Param description: Description of the dataset
        :Param assets: List of assets
        :Param contributors: List of contributors
        :Return: Dataset object if successful else raise exception
        """
        try:
            dataset = sy.Dataset(name=name, description=description, assets=assets, contributors=contributors)
            return dataset
        except Exception as e:
            raise Exception(f"{e}")
            
    def upload_dataset(self, client, dataset):
        """
        :Description: Upload a dataset
        :Param client: PySyft Client object
        :Param dataset: Dataset object
        :Return: True if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")
            client.upload_dataset(dataset)
            return True
        except Exception as e:
            raise Exception(f"{e}")
        
    def view_dataset(self, client, dataset_name: str):
        """
        :Description: View a dataset
        :Param client: PySyft Client object
        :Param dataset_name: Name of the dataset
        :Return: Dataset object if successful else raise exception
        """
        try:
            if client.user_role != ServiceRole.ADMIN:
                raise Exception("Permission denied.")
            datasets = client.datasets.get_all()
            dataset = next((ds for ds in datasets if ds.name == dataset_name), None)
            if dataset is None:
                raise Exception(f"Dataset '{dataset_name}' not found.")
            return dataset
        except Exception as e:
            raise Exception(f"{e}")    
        
    def view_datasets(self, client):
        """
        :Description: View all datasets
        :Param client: PySyft Client object
        :Return: List of datasets if successful else raise exception
        """
        try:
            datasets = client.datasets.get_all()
            dataset_list = []

            for dataset in datasets:
                dataset_details = {
                        "id": str(dataset.id),
                        "name": dataset.name,
                        "description": dataset.description.text,
                        "total_assets": len((dataset.assets))
                    }
                dataset_list.append(dataset_details)
            return dataset_list
        except Exception as e:
                raise Exception(f"Error retrieving datasets: {str(e)}")

    def view_assets(self, client, dataset_name: str):
        """
        :Description: View all assets in a dataset
        :Param client: PySyft Client object
        :Param dataset_name: Name of the dataset
        :Return: List of assets if successful else raise exception
        """
        try:
            datasets = client.datasets.get_all()            
            asset_list = []
            for dataset in datasets:
                if dataset.name == dataset_name:
                    for asset in dataset.assets:
                            # if isinstance(asset.mock, (list, np.ndarray)):
                            #     asset_mock = asset.mock.tolist() 
                            # else:
                            #     asset_mock = asset.mock if asset.mock is not None else "No Mock Data"
                        asset_details = {
                            "id": str(asset.id),
                            "name": asset.name,
                            "contributors":{
                                "id": [str(contributor.id) for contributor in asset.contributors],
                                "name": [contributor.name for contributor in asset.contributors],
                                "email": [contributor.email for contributor in asset.contributors],
                                "role": [contributor.role for contributor in asset.contributors]
                            },
                            "uploader": {
                                "id": str(asset.uploader.id),
                                "name": asset.uploader.name,
                                "email": asset.uploader.email,
                                "role": asset.uploader.role
                            },
                            "utc_timestamp": asset.created_at.utc_timestamp if asset.created_at else None,
                            # "mock":  asset_mock,
                            "mock": asset.mock,
                        }
                        asset_list.append(asset_details)
            return asset_list            
        except Exception as e:
                raise Exception(f"Error retrieving assets for dataset '{dataset_name}': {str(e)}")
            
    def remove_dataset(self,client, dataset_name: str):
        """
        :Description: Remove a dataset
        :Param client: PySyft Client object
        :Param dataset_name: Name of the dataset
        :Return: True if successful else raise exception
        """
        try:
                if client.user_role != ServiceRole.ADMIN:
                    raise Exception("Permission denied.")
                dataset_exists = self._dataset_exists(client,dataset_name)
                if dataset_exists is not None:
                    try:
                        client.api.dataset.delete(uid=dataset_exists.id)
                    except Exception as e:
                        raise Exception(f"{e}")                    
                    remaining_datasets = client.datasets
                    if dataset_exists not in remaining_datasets:
                        return True
                else:
                    raise Exception(f"Dataset '{dataset_name}' not found.")   
        except Exception as e:
                raise Exception(f"{e}")  
            

    #*******************************#
    #*        Private Methods      *#
    #*******************************#

    def private_method(func):
        def wrapper(*args, **kwargs):
            caller = inspect.stack()[1][3]
            if caller.startswith('_'):
                return func(*args, **kwargs)
            else:
                raise AttributeError("This method is private and cannot be accessed externally.")
        return wrapper
    

    @private_method
    def _user_exists(self, client, email):
        users = client.users.get_all()
        return next((user for user in users if user.email == email), None)       
    
    @private_method
    def _dataset_exists(self,client, dataset_name: str):
        try:
            all_datasets = client.datasets
            dataset_retrieved = next((ds for ds in all_datasets if ds.name == dataset_name), None)
            if dataset_retrieved is None:
                return None
            return dataset_retrieved
        except Exception as e:
            raise Exception(f"{e}")

