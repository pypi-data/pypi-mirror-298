import pandas as pd
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_salesforce(query, sf, shorten_column_names=True):
    """
    Query Salesforce and return results as a flattened pandas DataFrame.
    
    :param query: SOQL query string
    :param sf: Salesforce object
    :return: pandas DataFrame with flattened records
    """
    try:
        result = sf.query_all(query)
        records = result['records']
        
        # Flatten all records
        flattened_records = [flatten_record(record) for record in records]
        
        # Convert to DataFrame
        df = pd.DataFrame(flattened_records)
        logger.info(f"Columns before renaming: {df.columns}")

        # Removing the first part of the name before the first dot
        if shorten_column_names:
            df.columns = [shorten_columns(col) for col in df.columns]

        # Change from '.' to '_'
        df.columns = [rename_columns(col) for col in df.columns]
        logger.info(f"Columns after renaming: {df.columns}")
        
        return df
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

def flatten_record(record, parent_key='', sep='.'):
    """
    Flatten a nested dictionary into a single dictionary with dot-separated keys.
    
    :param record: Nested dictionary
    :param parent_key: String to prefix keys with
    :param sep: Separator to use between keys
    :return: Flattened dictionary
    """
    items = []
    for k, v in record.items():
        if k != 'attributes':
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_record(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)

# Change '.' to '_'
def rename_columns(col_name):
    return col_name.replace('.', '_')

def shorten_columns(col_name):
    """
    Rename columns by removing the first part of the name before the first dot.
    
    :param col_name: Original column name
    :return: Renamed column name
    """
    if '.' in col_name:
        return col_name.split('.')[-1]
    return col_name

# Split the Id from the Salesforce URL
def get_Id_from_SF_URL(url):
    return url.split('/')[-2]

# Get SF picklist options
def get_picklist_options(object_name, field_name, sf):
    # Describe the object to get field metadata
    describe = sf.__getattr__(object_name).describe()
    
    # Find the field and get its picklist options
    for field in describe['fields']:
        if field['name'] == field_name:
            picklist_values = [option['value'] for option in field['picklistValues']]
            return picklist_values
    return None

# Mass sending of Certificates of Attendance to Campaign Members
def send_coa_certificates(campaign_member_query, sf):
    campaign_member_df = query_salesforce(campaign_member_query, sf)

    def update_campaign_member(cm_id):
        try:
            sf.CampaignMember.update(cm_id, {'Send_Certificate_of_Attendance__c': False})
            sf.CampaignMember.update(cm_id, {'Certificate_of_Completion_Sent__c': False})
            sf.CampaignMember.update(cm_id, {'Send_Certificate_of_Attendance__c': True})
            return True
        except Exception as e:
            logger.error(f"Error updating CampaignMember {cm_id}: {str(e)}")
            return False

    # Update CampaignMembers one by one
    campaign_member_df['Update_Success'] = campaign_member_df['Id'].apply(update_campaign_member)

    # Print summary
    successful_updates = campaign_member_df['Update_Success'].sum()
    total_records = len(campaign_member_df)
    logger.info(f"Successfully updated {successful_updates} out of {total_records} CampaignMember records.") 


