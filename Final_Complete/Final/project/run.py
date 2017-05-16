import os
import main

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    main.app.run(host='127.0.0.1', port=port)

        #Credit for this code goes to http://stevenloria.com/hosting-static-flask-sites-for-free-on-github-pages/