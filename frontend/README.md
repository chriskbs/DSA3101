# DSA3101_library_frontend

This folder contains the frontend code for the library seat occupancy simulation system. The frontend interface is developed using Python Dash, alongside HTML and CSS concepts to enhance the visual appeal of the interface. The interactive graphs are generated using Plotly to enhance the user experience. 

## Folder Structure
The `assets` folder contains the images and icons that were used in the various pages. 

The `data` folder stores the data files generated from the input page as well as data files required for the simulation page. 

The other folder comprises Python scripts corresponding to each page of the web interface under development. 
## Getting Started

Assuming you have python and pip installed, or virtual environment equivalent, run the following commands to get started:

```bash
cd frontend
pip install -r requirements.txt
python3 app.py
```

You could access the frontend at http://localhost:8050

There is also a dockerfile, but it is mainly used with docker-compose for deployment purposes.

When you are debugging the code here, do turn on debug mode in Dash inside app.py.
```
app.run_server(host='0.0.0.0', debug=True)
```

## How app.py works and how to add a new page to app.py
The app.py script is meant as the control centre of the frontend application, any callback functions should be written here. We wrote comments to indicate which pages are involved for each callback function. Below shows how the application switches between different pages.
```
import input_page.input_page as ip
```
This imports the input_page.py that we have predefined in a different folder, which contains the html objects and page layout of the Input Page. With the script imported, we could access the layout defined in input_page.py using `ip.layout`, and the callback functions in app.py could refer to any html object in input_page.py using their id, which means it is important that there are no duplicated ids.
```
app.layout = html.Div(children = [dcc.Location(id = "url", refresh = False), html.Div(id = "output-div")])
```
Inside the app.layout there is a `dcc.Location` object with id “url” keeps track of the url location within the application. While the `html.Div` with id “output-div” will contain the current page layout. 
```
@app.callback(Output('output-div', 'children'), 
             Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/input':
        return ip.layout
```
This code demonstrates that if the url location is changed to /input, then the output-div’s children will be changed to the layout of input_page. This is how we execute the multi-page effect in the frontend application. Similarly, to update the current page shown in the application, create a new callback function with Output as the pathname of url. Any updates to the pathname of “url” will also trigger the display_page function above, and make the application display the respective layout.

**Therefore, when a new page is created, app.py needs to import the page, its callback functions have to be written inside the app.py script, and the page needs to be added to the display_page callback function shown above.**

## To run Docker Container 
1. Navigate to this folder via `cd` command in terminal
2. Build image using `docker build -t mydash .`
3. Run container using `docker run -d -p 9002:8050 mydash`
4. Navigate to http://localhost:9002 to view the interface
