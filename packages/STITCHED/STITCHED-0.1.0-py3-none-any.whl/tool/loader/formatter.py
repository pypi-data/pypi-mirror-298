import pandas as pd

class DataFrameFormatter:
    def __init__(self, config_df, dataframe, connection):
        self.df = dataframe
        self.conn = connection
        self.formatted_df = {}
        self.config = config_df
        self.source_cache = {}
        self.language_cache = {}
        self.max_source_id = self.__get_rowid('text_source')
        self.max_language_id = self.__get_rowid('language')
        self.start_text_id = 1
    # enable append mode to use one instance for separate files
    def format_for_sql(self, append = False):
        self.__format_dataset(append = append)
        self.__format_schema(append = append)
        self.__format_source()
        self.__format_language()
        self.__format_text()
        self.__format_label()
        return self.formatted_df
    def set_df(self, dataframe):
        self.df = dataframe
    def __format_dataset(self, append = False):
        dataset_data = {
            "dataset_id": [],
            'dataset_original_name': [],
            'dataset_name': []
        }
        if not append:
            self.dataset_id = self.__get_rowid("dataset")+1
            dataset_data['dataset_id'].append(self.dataset_id)
            dataset_data['dataset_original_name'].append(self.config['dataset_file_name'])
            dataset_data['dataset_name'].append(self.config['dataset_name'])
        dataset_df = pd.DataFrame(dataset_data)
        self.formatted_df['dataset'] = dataset_df
    def __format_schema(self, append = False):
        data = {
            "dataset_id": [],
            "label_name": []
        }
        if not append:
            self.label_columns = list((self.config['label_name_definition']).keys())
            data = {
                "dataset_id": [self.dataset_id] * len(self.label_columns),  # Repeat dataset_id for each label column
                "label_name": self.label_columns
            }
        table_schema = pd.DataFrame(data)
        self.formatted_df['schema'] = table_schema
    def __format_source(self):
        text_source_data = {
            "source_id": [],
            'source': []
        }
        if self.config['source'].startswith('@'):
            source = self.config['source'][1:]
            source_id = self.__search_source_rowid(source)
            if source_id > self.max_source_id:
                self.max_source_id = source_id
                text_source_data['source_id'].append(source_id)
                text_source_data['source'].append(source)
        # for a source col, fetch row_id by row
        else:
            source_col =self.df[self.config['source']]
            for source in source_col:
                source_id = self.__search_source_rowid(source)
                if source_id > self.max_source_id:
                    self.max_source_id = source_id
                    text_source_data['source_id'].append(source_id)
                    text_source_data['source'].append(source)
        text_source_df = pd.DataFrame(text_source_data)
        self.formatted_df['text_source'] = text_source_df
    def __format_language(self):
        language_data = {
            "language_id": [],
            'language': []
        }
        if self.config['language'].startswith('@'):
            language = self.config['language'][1:]
            language_id = self.__search_language_rowid(language)
            if language_id > self.max_language_id:
                self.max_language_id = language_id
                language_data['language_id'].append(language_id)
                language_data['language'].append(language)
        else:
            language_col =self.df[self.config['language']]
            for language in language_col:
                language_id = self.__search_language_rowid(language)
                if language_id > self.max_language_id:
                    self.max_language_id = language_id
                    language_data['language_id'].append(language_id)
                    language_data['language'].append(language)
        language_df = pd.DataFrame(language_data)
        self.formatted_df['language'] = language_df
    def __format_text(self):
        self.df["dataset_id"] = self.dataset_id
        text_col = self.config['text']
        self.df.rename(columns={
                    # 'id': 'text_id',
                    text_col: 'text'
                    }, inplace=True)
        # problem is that for separate files in the same dataset, it cannot be used
        # maybe can be solved by fetching the MAX text_id for this dataset
        # converter need to "remember" the dataset
        self.df['text_id'] = self.df.index + self.start_text_id
        # print(self.start_text_id)
        # print(len(self.df))
        self.start_text_id += len(self.df)
        table_text = self.df[['dataset_id', 'text_id', 'text']].drop_duplicates()
        if self.config['source'].startswith('@'):
            table_text['source_id'] = [self.source_cache.get(self.config['source'][1:])] * len(table_text)
        else:
            table_text['source_id'] = self.formatted_df['text_source'][self.config['source']].apply(lambda x: self.source_cache.get(x, 'n.a.'))

        if self.config['language'].startswith('@'):
            table_text['language_id'] = [self.language_cache.get(self.config['language'][1:])] * len(table_text)
        else:
            table_text['language_id'] = self.formatted_df['language'][self.config['language']].apply(lambda x: self.language_cache.get(x, 'n.a.'))

        self.formatted_df['text'] = table_text[['dataset_id', 'text_id', 'text','source_id','language_id']]

    def __format_label(self):
        table_label = pd.DataFrame(columns = ['dataset_id', 'text_id', 'label_name', 'label_value', 'label_definition'])
        for col, col_def in self.config['label_name_definition'].items():
            label_value_pair = {
                'dataset_id': self.df['dataset_id'].values,
                'text_id': self.df['text_id'].values,
                'label_name': [col] * len(self.df),
                'label_value': self.df[col].values,
                'label_definition': [col_def] * len(self.df)
            }
            temp_df = pd.DataFrame(label_value_pair)
            table_label = pd.concat([table_label, temp_df], axis=0, ignore_index=True)
        self.formatted_df['label'] = table_label
        assert self.formatted_df['label'].shape[0] == self.formatted_df['text'].shape[0] * len(self.config['label_name_definition'].items())
    def __search_source_rowid(self, source):
        # first check the dic, which consists of
        # #1.existing source-id pairs that have been queried
        # #2.non-existing pairs that have been created in the dic
        if source in self.source_cache:
            return self.source_cache[source]
        # then try to query it form the db
        c = self.conn.cursor()
        c.execute("SELECT source_id FROM text_source WHERE source = ?", (source,))
        source_id = c.fetchone()
        if source_id is not None:
            self.source_cache[source] = source_id[0]
            return source_id[0]
        # create new source_id
        else:
            # instead of increasing self.max_source_id here,
            # put the logic outside so that the table can be adjusted
            self.source_cache[source] = self.max_source_id + 1
            return self.source_cache[source]
    def __search_language_rowid(self, language):
        # first check the dic
        if language in self.language_cache:
            return self.language_cache[language]
        # then try to query it form the db
        c = self.conn.cursor()
        c.execute("SELECT language_id FROM language WHERE language = ?", (language,))
        language_id = c.fetchone()
        if language_id is not None:
            self.language_cache[language] = language_id[0]
            return language_id[0]
        # create new
        else:
            self.language_cache[language] = self.max_language_id + 1
            return self.language_cache[language]
    def __get_rowid(self, table_name):
        '''Get the ID of the last inserted record in the specified table'''
        c = self.conn.cursor()
        c.execute("SELECT MAX(rowid) FROM {}".format(table_name))
        last_inserted_id = c.fetchone()[0]
        return last_inserted_id if last_inserted_id is not None else 0


# ### Configuration

# In[3]:


## information we need to know from Config file
# dataset_id = 1
# label_columns = ["subtask_a", "subtask_b", "subtask_c"]
# source_id = 1

# def get_rowid(conn, table_name):
#     '''Get the ID of the last inserted record in the specified table
#     parameter conn: database connection'''
#     c = conn.cursor()
#     c.execute("SELECT MAX(rowid) FROM {}".format(table_name))
#     last_inserted_id = c.fetchone()[0]
#     return last_inserted_id

# def create_dataset_id(conn):
#     last_inserted_id = get_rowid(conn, "dataset")
#     return last_inserted_id + 1

# def get_text_source_id(conn, text_source):
#     last_inserted_id = get_rowid(conn, "text_source")
#     return last_inserted_id + 1

# def get_language_id(conn, language):
#     last_inserted_id = get_rowid(conn, "language")
#     return last_inserted_id + 1


# Create table ***Schema***

# In[4]:


# Create a DataFrame with the specified columns
# data = {
#     "dataset_id": [dataset_id] * len(label_columns),  # Repeat dataset_id for each label column
#     "label_name": label_columns
# }
#
# table_schema = pd.DataFrame(data)

# def generate_temporary_schema(label_columns):
#     data = {
#         "dataset_id": [dataset_id] * len(label_columns),  # Repeat dataset_id for each label column
#         "label_name": label_columns
#     }
#     table_schema = pd.DataFrame(data)
#     return table_schema

# def call_generate_temporary(table_name, *args):
#     function_name = f'generate_temporary_{table_name}'
#     if function_name in globals() and callable(globals()[function_name]):
#         globals()[function_name](*args)
#     else:
#         print("Unsupported table name.")


# In[5]:


# table_schema


# In[6]:


# df["dataset_id"] = dataset_id
# df.rename(columns={'id': 'text_id',
#                    'tweet':'text'
#                    }, inplace=True)



# In[7]:


# df


# Create Table ***text***

# In[8]:


# table_text = df[['dataset_id', 'text_id', 'text']].drop_duplicates()


# In[9]:


# table_text['source_id'] = source_id


# In[10]:


# table_text


# Create Table ***label***

# In[11]:


# table_label = pd.DataFrame(columns = ['dataset_id', 'text_id', 'label_name', 'label_value'])


# In[12]:

#
# table_label


# In[13]:


# for col in label_columns:
#     label_value_pair = {
#     'dataset_id': df['dataset_id'].values,
#     'text_id': df['text_id'].values,
#     'label_name': [col] * len(df),
#     'label_value': df[col].values
#     }
#     temp_df =  pd.DataFrame(label_value_pair)
#     table_label = pd.concat([table_label, temp_df], axis=0, ignore_index=True)


# In[14]:


# table_label


# ### To-be-discussed

# 1. What to include in the Config JSON file, in which format?
# 2. How to handle the data source, also ask the user to include in the config file?
#     - When coming from different sources?
# 3. label explaination
#     - as a tuple in the config file (label_name, label_explaination), or?

# In[14]:




