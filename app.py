from api import app,db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import get_all_users_resolver,get_user_by_id,get_all_csv_files
from api.mutation import create_user_resolver,upload_csv_file,delete_csv_file


query = ObjectType("Query")
mutation = ObjectType("Mutation")
query.set_field("getAllUsers", get_all_users_resolver)
query.set_field("getUserById", get_user_by_id )
query.set_field("getAllCsvFiles",get_all_csv_files)
mutation.set_field("createUser",create_user_resolver)
mutation.set_field("uploadCsvFile",upload_csv_file)
mutation.set_field("DeleteCsvFileUrl",delete_csv_file)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs,query,mutation, snake_case_fallback_resolvers
)
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route('/')
def index():
    return 'Healthy'

if __name__ == '__main__':
    app.run(port=8800)
