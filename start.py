from flask import Flask, jsonify, abort, make_response, request, url_for, redirect
from convert import convert

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    return 'Hello, World!'

@app.route('/help', methods=['GET', 'POST'])
def help():
    urls = [
            {
                'urn': url_for('.test', _external=True),
                'title': 'GET/POST: Returns hello, world',
            },
            {
                'urn': url_for('.help', _external=True),
                'title': 'GET help (this document)',
            },

            {
                'urn': url_for('.csv', _external=True),
                'title': 'POST (csv)',
                'expected input': '{ "filename": "The filename to be saved, "path": "The path of where to save the filename", "input": "A csv string" }'
            },
    ]
    return jsonify(urls)

@app.route('/csv', methods=['GET', 'POST'])
def csv():
    try:
        if request.method == 'GET':
            return jsonify(
                {
                    'success': False,
                    'error': 'Please use post request'
                }
            )

        else:
            form = request.get_json()
            filename = form.get('filename' or '')
            path = form.get('path' or '')
            csv = form.get('input' or '')
            output_path = convert(path, filename, csv)

            print('POST REQUEST: \n', form)
            return jsonify({
                'success': True,
                'filename': filename,
                'path': path,
                'output_path': output_path,
                'length': len(csv),
                # 'input': form
            })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        })


# main driver function
if __name__ == '__main__':
    #If we enter using 'python start.py' we need app.run. If we run with 'flask run' then we do not.
    # app.run(debug=True, port=5000, threaded=True)
    app.run(debug=True, port=5000, threaded=True, host="dirks-mbp")
    # threaded: is not default and needed to make internal api http requests
