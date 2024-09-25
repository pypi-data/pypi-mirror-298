from lmanage.looker_auth import LookerAuth
from lmanage.configurator.user_attribute_configuration import create_and_assign_user_attributes as cuap
from lmanage.configurator.folder_configuration import create_and_provision_instance_folders as cfp, create_instance_folders as cf
from lmanage.configurator.user_group_configuration import create_instance_groups as gc, create_instance_roles as up, create_role_base as rc
from lmanage.configurator.content_configuration import clean_instance_content as ccp, create_looks as cl, create_dashboards as cd, create_boards as cb
from lmanage.utils import logger_creation as log_color


class LookerProvisioner():
    def __init__(self, ini_file, verbose):
        self.sdk = LookerAuth().authenticate(ini_file)
        self.logger = log_color.init_logger(__name__, testing_mode=verbose)

    def provision(self, metadata):
        ###############
        # Role Config #
        ###############
        # Create Permission and Model Sets
        # rc.CreateRoleBase(permissions=metadata['permission_set_metadata'],
        #                   model_sets=metadata['model_set_metadata'], sdk=self.sdk, logger=self.logger).execute()

        #################
        # Folder Config #
        #################
        # CREATE NEW FOLDERS
        # folder_objects = cf.CreateInstanceFolders(
        #     folder_metadata=metadata['folder_metadata'], sdk=self.sdk, logger=self.logger)
        # created_folder_metadata = folder_objects.create_folders()

        # CREATE FOLDER TO FOLDER Dict
        # folder_mapping_obj = folder_objects.create_folder_mapping_dict(
        #     folder_metadata=created_folder_metadata)
        
        # print(folder_mapping_obj)
        folder_mapping_obj ={'1': '1', '2': '6822', '3': '6823', '4': '6824', '5': '6825', '6': '6826', '7': '6827', '8': '6828', '9': '6829', '10': '6830', '11': '6831', '12': '6832', '13': '6833', '14': '6834', '15': '6835', '16': '6836', '18': '6837', '19': '6838', '20': '6839', '21': '6840', '22': '6841', '23': '6842', '24': '6843', '25': '6844', '26': '6845', '27': '6846', '28': '6847', '29': '6848', '30': '6849', '31': '6850', '32': '6851', '34': '6852', '35': '6853', '36': '6854', '37': '6855', '38': '6856', '39': '6857', '40': '6858', '41': '6859', '42': '6860', '43': '6861', '44': '6862', '45': '6863', '46': '6864', '47': '6865', '48': '6866', '50': '6867', '51': '6868', '52': '6869', '53': '6870', '54': '6871', '55': '6872', '56': '6873', '57': '6874', '58': '6875', '59': '6876', '60': '6877', '61': '6878', '62': '6879', '63': '6880', '64': '6881', '66': '6882', '67': '6883', '68': '6884', '69': '6885', '70': '6886', '71': '6887', '72': '6888', '73': '6889', '74': '6890', '75': '6891', '76': '6892', '77': '6893', '78': '6894', '79': '6895', '80': '6896', '82': '6897', '83': '6898', '84': '6899', '85': '6900', '86': '6901', '87': '6902', '88': '6903', '89': '6904', '90': '6905', '91': '6906', '92': '6907', '93': '6908', '94': '6909', '95': '6910', '96': '6911', '98': '6912', '99': '6913', '100': '6914', '101': '6915', '102': '6916', '103': '6917', '104': '6918', '105': '6919', '106': '6920', '107': '6921', '108': '6922', '109': '6923', '110': '6924', '111': '6925', '112': '6926', '114': '6927', '115': '6928', '116': '6929', '117': '6930', '118': '6931', '119': '6932', '120': '6933', '121': '6934', '122': '6935', '123': '6936', '124': '6937', '125': '6938', '126': '6939', '127': '6940', '128': '6941', '130': '6942', '131': '6943', '132': '6944', '133': '6945', '134': '6946', '135': '6947', '136': '6948', '137': '6949', '138': '6950', '139': '6951', '140': '6952', '141': '6953', '142': '6954', '143': '6955', '144': '6956', '146': '6957', '147': '6958', '148': '6959', '149': '6960', '150': '6961', '151': '6962', '152': '6963', '153': '6964', '154': '6965', '155': '6966', '156': '6967', '157': '6968', '158': '6969', '159': '6970', '160': '6971', '162': '6972', '163': '6973', '164': '6974', '165': '6975', '166': '6976', '167': '6977', '168': '6978', '169': '6979', '170': '6980', '171': '6981', '172': '6982', '173': '6983', '174': '6984', '175': '6985', '176': '6986', '178': '6987', '179': '6988', '180': '6989', '181': '6990', '182': '6991', '183': '6992', '184': '6993', '185': '6994', '186': '6995', '187': '6996', '188': '6997', '189': '6998', '190': '6999', '191': '7000', '192': '7001', '194': '7002', '195': '7003', '196': '7004', '197': '7005', '198': '7006', '199': '7007', '200': '7008', '201': '7009', '202': '7010', '203': '7011', '204': '7012', '205': '7013', '206': '7014', '207': '7015', '208': '7016', '210': '7017', '211': '7018', '212': '7019', '213': '7020', '214': '7021', '215': '7022', '216': '7023', '217': '7024', '218': '7025', '219': '7026', '220': '7027', '221': '7028', '222': '7029', '223': '7030', '224': '7031'}

        ################
        # Group Config #
        ################
        # CREATE NEW GROUPS FROM YAML FILE TEAM VALUES
        # gc.CreateInstanceGroups(
        #     folders=created_folder_metadata,
        #     user_attributes=metadata['user_attribute_metadata'],
        #     roles=metadata['role_metadata'],
        #     sdk=self.sdk,
        #     logger=self.logger).execute()

        ###########################
        # Folder Provision Config #
        ###########################
        # CREATE NEW GROUPS FROM YAML FILE TEAM VALUES
        # cfp.CreateAndProvisionInstanceFolders(
        #     folders=created_folder_metadata,
        #     sdk=self.sdk, logger=self.logger).execute()

        ###############
        # Role Config #
        ###############
        # up.CreateInstanceRoles(roles=metadata['role_metadata'],
        #                        sdk=self.sdk,
        #                        logger=self.logger).execute()

        #########################
        # User Attribute Config #
        #########################
        # FIND UNIQUE USER ATTRIBUTES AND ATTRIBUTE TO TEAM
        # cuap.CreateAndAssignUserAttributes(
        #     user_attributes=metadata['user_attribute_metadata'],
        #     sdk=self.sdk,
        #     logger=self.logger).execute()

        ############################
        # Content Transport Config #
        ############################
        # EMPTY TRASH CAN OF ALL DELETED CONTENT
        ccp.CleanInstanceContent(sdk=self.sdk, logger=self.logger).execute()

        # FIND LOOKS AND REMAKE THEM
        # cl.CreateLooks(
        #     sdk=self.sdk,
        #     folder_mapping=folder_mapping_obj,
        #     content_metadata=metadata['look_metadata'],
        #     logger=self.logger).execute()

        # Find DASHBOARDS AND REMAKE THEM
        cd.CreateDashboards(
            sdk=self.sdk,
            folder_mapping=folder_mapping_obj,
            content_metadata=metadata['dashboard_metadata'],
            logger=self.logger).execute()
