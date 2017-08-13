# SearchTool

This tool is designed to help users retrieve relevant blog articles. It sits on top of existing search engines to further filter results to ensure relevance. 

---

## Getting started
To get started with this tool, download using the following command:

```
git clone https://github.com/zedrem/SearchTool
```

### Prerequisites
Prior to running, you will need to have Python installed and access to a MongoDB implementation.

* Python - tested with version 3.6.1
* MongoDB - we have installed Mongo locally from [MongoDB](https://www.mongodb.com/). However, you may also use a hosted solution such as [Mongo Lab](https://mlab.com/)

Alternatively, you can use an online IDE like [Cloud9](https://c9.io/) which comes with Python pre-installed. Instructions for setting up Mongo in Cloud9 can be found [here](https://community.c9.io/t/setting-up-mongodb/1717)

### Installing requirements
Once you have Python and Mongo ready to go, you need to install the required Pip packages. These can be found in the `requirements.txt` file. You may install them manually using:

```
pip install -r requirements.txt
```

or run the provided `MAKEFILE`.

### Connecting to the database
Next, edit `db_config.json`, located in the config directory. Add the path to your database, and your desired database name.

```
{
	"db_url": "mongodb://127.0.0.1/",
	"db_client": "relevance-querying"
}
```

### The setup file
Finally, run the setup file by navigating to the root directory in your terminal and using the command below:

```
python ./setup.py
```

This setup file tests the connection to your database, and then loads the example indicators and default config settings. More information on what these settings are can be found in the applications documentation (in the `/docs` directory). The application is now setup and ready to use.

---

## Running the application
Read the user guide in `/docs` for a brief description of how to use this tool.

---

## License
This application has been released under the MIT licese. More information can be found in the `/LICENSE` file.

---

## Questions?
If you have any questions, please contact the projects author via the issues section, or by emailing: ashley.williams@pg.canterbury.ac.nz