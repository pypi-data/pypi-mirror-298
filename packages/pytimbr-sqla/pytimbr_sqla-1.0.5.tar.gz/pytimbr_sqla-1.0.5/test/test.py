# pip install git+https://github.com/WPSemantix/timbr_python_SQLAlchemy
# make new version without publish
# pip uninstall pytimbr-sqla
# pip install pip install ../dist/pytimbr_sqla-<X>.<X>.<X>.tar.gz

from sqlalchemy.engine import create_engine
from TCLIService.ttypes import TOperationState

if __name__ == '__main__':
  # HTTPS example

  # hostname = 'staging.timbr.ai'
  hostname = 'demo-env.timbr.ai'
  port = '443'
  protocol = 'https'
  # ontology = 'timbr_e2e_tests'
  ontology = 'timbr_demo_v1'
  username = 'token'
  # password = 'tk_f283d1885598e6a79b7a56265484174e709c73d72abdaaa0025990a43f4e981d'
  password = 'tk_d070e658d60e321bea21961590b26157f7ce1b3b6a32b1bf963d2b44782df558'
  connect_args = {
    'configuration': {
      'set:hiveconf:hiveMetadata': 'true',
      # 'set:hiveconf:active_datasource': '<datasource_name>',
      # 'set:hiveconf:active_datasource': 'mysql',
      'set:hiveconf:active_datasource': 'bigquery',
      'set:hiveconf:queryTimeout': '20',
    },
  }


  try:
    # # example file

    # # Create new sqlalchemy connection
    # engine = create_engine(f"timbr+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}")

    # # Connect to the created engine
    # conn = engine.connect()

    # # Execute a query
    # query = "SHOW CONCEPTS"
    # concepts = conn.execute(query).fetchall()

    # # Display the results of the execution
    # for concept in concepts:
    #   print(concept)




    # # async pyhive

    # # Create new sqlalchemy connection
    # engine = create_engine(f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args={'configuration': {'set:hiveconf:hiveMetadata': 'true'}})

    # # Connect to the created engine
    # conn = engine.connect()
    # dbapi_conn = engine.raw_connection()
    # cursor = dbapi_conn.cursor()

    # # Execute a query
    # query = "SHOW CONCEPTS"
    # cursor.execute(query)

    # # Check the status of this execution
    # status = cursor.poll().operationState
    # while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
    #   status = cursor.poll().operationState

    # # Display the results of the execution
    # results = cursor.fetchall()
    # print(results)





    # sync pyhive

    # Create new sqlalchemy connection
    engine = create_engine(f"timbr+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args=connect_args)

    # Connect to the created engine
    conn = engine.connect()

    # Use the connection to execute a query
    # query = "SHOW CONCEPTS"
    # query = "select sleep(20)"
    query = "SHOW SCHEMAS"
    results = conn.execute(query).fetchall()

    # Display the results of the execution
    print(results)
  except Exception as e:
    print(e)