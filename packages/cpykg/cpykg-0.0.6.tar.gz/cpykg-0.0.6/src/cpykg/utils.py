import pandas as pd
import re
from py2neo import Graph
import getpass as gp
from yfiles_jupyter_graphs_for_neo4j import Neo4jGraphWidget
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget

from importlib import resources

# Get a list of all CSV files in the data folder
def list_csv_files():
    csv_files = []
    package_dir = resources.files('cpykg.data')
    for file in package_dir.iterdir():
        if file.suffix == '.csv':
            csv_files.append(file.name)
    return csv_files

# Return a single Dataset from the data folder by name
def read_csv_file(filename):
    if not filename.endswith('.csv'):
        raise ValueError("File must be a CSV")
    
    package_dir = resources.files('cpykg.data')
    file_path = package_dir / filename
    
    with file_path.open('r') as file:
        df = pd.read_csv(file,index_col=0)
    return df

# Get all of the datasets loaded in
def load_datasets():
    global AISecKG, MetaQA_KG, R25KG_rare, SDKG_Dis11
    AISecKG = read_csv_file('AISecKG.csv')
    MetaQA_KG = read_csv_file('MetaQA_KG.csv')
    R25KG_rare = read_csv_file('R25KG_rare.csv')
    SDKG_Dis11 = read_csv_file('SDKG_Dis11.csv')
    
    print('Following Datasets created: AISecKG, MetaQA_KG, R25KG_rare, SDKG_Dis11')


def replace_leading_numbers(name):
    num_to_word = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
}
    def replace(match):
        return ' '.join(num_to_word[digit] for digit in match.group(0)) + ' '
    return re.sub(r'^\d+', replace, str(name)).strip()

# Normalize dataset for neo4j conversion
def neo_norm(data_set):
    cols = list(data_set.columns)
    
    for i in cols:
        data_set[i] = data_set[i].apply(replace_leading_numbers)
        data_set[i] = data_set[i].str.replace(r'[^\w]', '_', regex=True)
        data_set[i] = data_set[i].str.lower()
        
    return data_set

def generate_cypher_queries(data):
    
    csv_data = neo_norm(data)
    
    values = set(set(csv_data['H']) | set(csv_data['T']))
    
    queries = []
    relations_query = []
    
    for value in values:
        # Replace spaces with underscores and remove any special characters
        clean_value = ''.join(e for e in value.replace(" ", "_") if e.isalnum() or e == "_")
        # Create the Cypher query
        query = f"CREATE ({value}:Entity {{name: '{value}', id: '{clean_value.lower()}'}})"
        queries.append(query)
        
    for index, row in csv_data.iterrows():
        if index == 0:
            relations_query.append(f'CREATE ({row["H"]})- [:{row["R"]}]-> ({row["T"]}),')
        elif index != (len(csv_data)-1):
            relations_query.append(f'({row["H"]})- [:{row["R"]}]-> ({row["T"]}),')
        else:
            relations_query.append(f'({row["H"]})- [:{row["R"]}]-> ({row["T"]})')

    
    return queries, relations_query, values

# Create the neo4j Graph using a connection
def neo_graph(data):
    global user, pw
    # Connect to Neo4j
    user = str(input('neo4j Username: '))
    pw = gp.getpass('neo4j Password:' )
    connector = 'bolt://localhost:7687'
    graph = Graph(connector, auth=(user, pw))
    
    print('Connecting through', connector)
    
    my_list, my_rels, vals = generate_cypher_queries(data)
    graph.run('MATCH (n) DETACH DELETE n')
    
    query = str()
    for i in range(0,len(my_list)):
        query += my_list[i]
    for j in range(0,len(my_rels)):
        query += my_rels[j]
    
    graph.run(query)
    
    return

# Visulaize 500 nodes of the graph made with neo4j using graphwidget
def vis_neo():
    print('Visualize up to 500 nodes')
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user, pw))
    g = Neo4jGraphWidget(driver)
    g.show_cypher("MATCH (s)-[r]->(t) RETURN s,r,t LIMIT 500")
    return

