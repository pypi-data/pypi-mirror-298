## Title

QSEA refers to the Qlik Sense Engine API. 

## Description

QSEA is designed to automate basic operations with Qlik Sense Enterprise apps in a Pythonic way. With QSEA, you can quickly view and edit variables, master measures, dimensions and sheet charts. For example, you can replace variables in all master measures of your app with just one line of code:

```python
for ms in App.measures: ms.update(definition = replace(ms.definition, '$(var1)', '$(var2)'))
```
or quickly move all measures from one app to another:

```python
for ms in source_app.measures: ms.copy(target_app)
```
or copy a sheet with all charts from one app to another:
```python
source_app.sheets['Source_sheet_name'].copy(target_app)
```

## Installation

```python
pip install qsea
```

## Table of Contents
- [Getting started](#getting-started)
- [Full Guide](#full-guide)
    - [App class](#app-class)
        - [App.load()](#appload)
        - [App.save()](#appsave)
        - [App.reload_data()](#appreload_data)
        - [App.children](#appchildren)
    - [AppChildren class](#appchildren-class)
        - [AppChildren add](#appchildrenadd)
    - [Variable class](#variable-class)
        - [Variable properties](#variable-properties)
        - [Variable.update()](#variableupdate)
        - [Variable.delete()](#variabledelete)
        - [Variable.rename()](#variablerename)
        - [Variable.get_layout()](#variableget_layout)
    - [Measure class](#measure-class)
        - [Measure properties](#measure-properties)
        - [Measure.copy()](#measurecopy)
        - [Measure.update()](#measureupdate)
        - [Measure.delete()](#measuredelete)
        - [Measure.rename()](#measurerename)
        - [Measure.get_layout()](#measureget_layout)
        - [Measure.get_properties()](#measureget_properties)
    - [Dimension class](#dimension-class)
        - [Dimension properties](#dimension-properties)
        - [Dimension.copy()](#dimensioncopy)
        - [Dimension.update()](#dimensionupdate)
        - [Dimension.delete()](#dimensiondelete)
        - [Dimension.rename()](#dimensionrename)
        - [Dimension.get_layout()](#dimensionget_layout)
    - [Sheet class](#sheet-class)
        - [Sheet properties](#sheet-properties)
        - [Sheet.copy()](#sheetcopy)
        - [Sheet.load()](#sheetload)
        - [Sheet.clear()](#sheetclear)
        - [Sheet.get_layout()](#sheetget_layout)
    - [Field class](#field-class)
        - [Field properties](#field-properties)
    - [Bookmark class](#bookmark-class)
        - [Bookmark properties](#bookmark-properties)
    - [Object class](#object-class)
        - [Object properties](#object-properties)
        - [Object.export_data()](#objectexport_data)
        - [Object.copy()](#objectcopy)
        - [Object.load()](#objectload)
        - [Object.get_layout()](#objectget_layout)
    - [ObjectChildren class](#objectchildren-class)
    - [ObjectMeasure class](#objectmeasure-class)
        - [ObjectMeasure properties](#objectmeasure-properties)
        - [ObjectMeasure.update()](#objectmeasureupdate)
        - [ObjectMeasure.delete()](#objectmeasuredelete)
    - [ObjectDImension class](#objectdimension-class)
        - [ObjectDimension properties](#objectdimension-properties)
        - [ObjectDimension.update()](#objectdimensionupdate)
        - [ObjectDimension.delete()](#objectdimensiondelete)
- [Roadmap](#roadmap)
- [License](#license)

## Getting started

QSEA uses the Qlik Sense Engine API via the Qlik Sense Proxy Service as its main tool, so you'll need a Virtual Proxy and a JWT key to start working with QSEA. Please refer to the following links for help.

How to set up JWT authentication
https://community.qlik.com/t5/Official-Support-Articles/Qlik-Sense-How-to-set-up-JWT-authentication/ta-p/1716226

Setting up a Virtual Proxy
https://help.qlik.com/en-US/sense-admin/February2024/Subsystems/DeployAdministerQSE/Content/Sense_DeployAdminister/QSEoW/Administer_QSEoW/Managing_QSEoW/create-virtual-proxy.htm


Your credentials should look something like this
```python
header_user = {'Authorization': 'Bearer <Very long API KEY>'}
qlik_url = "wss://server.domain.com[/virtual proxy]/app/"
```

Now we can connect to the Qlik Server:
```python
conn = qsea.Connection(header_user, qlik_url)
```

Let's create an App object, which represents the application in Qlik Sense.
```python
app = qsea.App(conn, 'MyAppName')
```

By default the App class object is almost empty. Use the `load()` function to make use of it:
```python
app.load()
```

Now all variables, master measures, and dimensions are uploaded to our App object. We can access them by their name:
```python
var = app.variables['MyVar']
var.definition
```

```python
ms = app.measures['MyMeasure']
ms.label_expression
```

Or, we can overview their properties via a pandas DataFrame.
```python
app.dimensions.df
```

Let's create a new measure:
```python
app.measures.add(name = 'MyMeasure', definition = 'sum(Sales)')
```

or update a variable:
```python
var.update(definition = 'sum(Sales)')
```

Save the app to ensure that the changes are reflected in the real Qlik Sense application.
```python
app.save()
```

Let's copy the set of master dimensions into a new app:
```python
source_app = qsea.App(conn, 'Source AppName')
target_app = qsea.App(conn, 'Target AppName')
source_app.dimensions.load()
target_app.dimensions.load()

for dim in source_app.dimensions:
    if dim.name not in [target_dim.name for target_dim in target_app.dimensions]: 
        dim.copy(target_app = target_app)

target_app.save()
```

Besides master measures, master dimensions, and variables, tables and charts in the App can also be uploaded.
```python
app.load()
sh = app.sheets['MySheet']
sh.load()
for obj in sh.objects:
    obj.load()
    for ms on obj.measures:
        print(ms.definition)
```

Objects and entire sheets can be copied to another app. While it is possible to copy sheets via the Qlik Sense interface, in some cases this can cause problems if the set of the master measures/dimensions in the source and target apps are different. Qsea allows to choose whether to match master measure IDs or names.
```python
source_app = qsea.App(conn, 'Source AppName')
target_app = qsea.App(conn, 'Target AppName')
source_app.load()
target_app.load()

source_sh = source_app.sheets['SheetToCopy']
source_sh.copy(target_app = target_app)

source_obj = source_app.sheets['SheetWithObject'].objects['SourceObjectID']
source_obj.copy(target_app = target_app, target_sheet = target_app.sheets['TargetSheet'])

target_app.save()
```

For unknown reasons, on certain instances of Qlik Sense, changes in the App may not be visible in the Qlik Sense interface. The usual workaround is to make a new copy of the Application (via QMC or Hub). Usually, all changes can be seen in the copy.

Note that as it stands, only basic properties, such as names, definitions, and a couple of others, can be accessed via the qsea module.

Most read-only operations (such as loading apps) can be performed on published apps. However, it is recommended to modify objects only in unpublished apps.

It's highly recommended to make a backup copy of your application.

Good luck!

## Full Guide

### Connection class
The class that represents a dictionary of websocket connections to Qlik Sense Engine API
Since one websocket connection can be used only for one app, this class is used to handle all websocket connections
New websocket connections are created automatically when a new app object is created

Note that the Qlik Sense Engine API has a limit of active parallel connections. Since there is no way to terminate the existing connection (except restarting the proxy server that is generally unacceptable), one have to wait for the Qlik Sense Engine to terminate some of the old sessions.
There is no way to reconnect to an existing connection if the Connection class object is recreated. Thus, it is highly recommended to avoid recreating the Connection class object in order to avoid reaching the limit of active connections.

### App class
The class, representing the Qlik Sense application. This is the main object to work with. The class is empty when created; run the `load()` function to make use of it.

#### App.load()
Loads data from the Qlik Sense application into an App object.

Args:
* depth (int): depth of loading
    - 1 - app + variables, measures, sheets, fields, dimensions (default value)
    - 2 - everything from 1 + sheet objects (tables, sharts etc.)
    - 3 - everything from 2 + object dimensions and measures

Different levels can be useful when working with large apps, as a full load can be time-consuming. Only dimensions and measures from standard Qlik Sense charts are uploaded. Uploading dimensions from filter panes is currently not supported.

```python
App.load(level = 3)
```

#### App.save()
You have to save the App object for the changes to be reflected in the Qlik Sense Application. Note that it is recommended to modify objects only in unpublished apps.
```python
App.save()
```

#### App.reload_data()
Starts the script of reloading data into the Qlik Sense Application.
```python
App.reload_data()
```

#### App.children
app.load(level = 1) creates several objects of AppChildren class

### AppChildren class
The class contains collections of master objects in the Qlik Sense Application:
* `app.variables`: a collection of Variable class objects, representing the variables of the Qlik Sense application
* `app.measures`: a collection of Measure class objects, representing the master measures of the Qlik Sense application
* `app.dimensions`: a collection of Dimension class objects, representing the master dimensions of the Qlik Sense application
* `app.sheets`: a collection of Sheet class objects, representing the sheets of the Qlik Sense application 
* `app.fields`: a collection of Field class objects, representing the fields of the Qlik Sense application

You can access the main information about each group of objects in a pandas DataFrame via the `.df` attribute:
```python 
app.variables.df
app.measures.df
``` 
#### AppChildren.add()
Use the `add()` function to add new variables, master measures, master dimensions or sheets to the app. 

Args:
* name (str): Name of the object to be created.
* definition (str): Definition of the object to be created.
* description (str, optional): Description of the object to be created. Defaults to ''.
* label (str, optional): Label of the object to be created. Defaults to ''.
* label_expression (str, optional): Label expression of the object to be created. Defaults to ''.
* format_type (str, optional): Format type of the object to be created. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec (int, optional): Number of decimals of the object to be created. Defaults to 10.
* format_use_thou (int, optional): Use thousands separator for the object to be created. Defaults to 0.
* format_dec (str, optional): Decimal separator for the object to be created. Defaults to ','.
* format_thou (str, optional): Thousands separator for the object to be created. Defaults to ''.
* base_color (str, optional): Base color (hex) for the object to be created. Defaults to None.
* source (variable, measure or dimension, optional): Source object for the object to be created. Defaults to None.

Returns: ID of the object created, if created successfully, None otherwise.
Only parameters applicable to the specific class will be used
```python
app.variables.add(name = 'MyVar', definition = 'sum(Sales)')
app.measures.add(name = 'MyFunc', definition = 'sum(Sales)', format_type = 'F')
app.dimensions.add(name = 'MyDim', definition = 'Customer')
app.measures.add(source = App1.measures['MyFunc'])
app.sheets.add(name = 'MySheet')
```

### Variable class
The class represents variables of the application and is a member of the App.variables collection. You can access a specific variable by its name or iterate through them:
```python
var = app.variables['MyVar']
print(var.definition)

for var in app.variables:
    if var.definition == 'sum(Sales)': var.update(name = 'varSales')
```
#### Variable properties
* name: this is the name of the variable you generally use in the Qlik Sense interface
* definition: the formula behind the variable
* description: the description of the variable
* auxiliary
    - handle: the internal handle of the object in the Qlik Sense Engine API; can be  used to access the variable via the `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the variable
    - parent: App-children object; you can access the App class object like this `var.parent.parent`
    - created_date: creation date of the variable, as stored in Qlik Sense
    - modified_date: date of the last modification of the variable, as stored in Qlik Sense
    - script_created: True if the variable is created via the application load script, False if not.

#### Variable.update()
Updates the variable on the Qlik Sense Server

Args:
* definition (str, optional): new definition of the variable (leave `None` to keep the old value)
* description (str, optional): new description of the variable (leave `None` to keep the old value)

Returns:
    True if the variable was updated successfully, False otherwise
```python
var = app.variables['MyVar']
var.update(definition = 'sum(Sales)')
app.save()
```

#### Variable.delete()
Deletes the variable from the Qlik Sense Server

Returns:
    True if the variable was deleted successfully, False otherwise

```python
var = app.variables['MyVar']
var.delete()
app.save()
```

#### Variable.rename()
Renames the variable on the Qlik Sense Server. Since there is no direct method to rename the variable, it essentially  deletes the variable with the old name, and creates a new one, with the new name.

Returns:
    True if the variable is renamed successfully, False otherwise

```python
var = app.variables['MyVar']
var.rename('MyVarNewName')
app.save()
```

#### Variable.get_layout()
Returns the json layout of the variable; a shortcut to the GetLayout method of the Engine API

```python
var.get_layout()
```

### Measure class
The class represents master measures of the application and is a member of the App.measures collection. You can access a specific measure by its name or iterate through them.
```python
ms = app.measures['MyMeasure']
print(ms.definition)

for ms in app.measures:
    if ms.definition == 'sum(Sales)': ms.update(name = 'Sales')
```
#### Measure properties
* name: the name of the measure you generally use in the Qlik Sense interface
* definition: the formula behind the measure
* description: the description of the measure
* label: the label of the measure, as it appears in charts
* label_expression: the label expression of the measure
* format_type: Format type of the object
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec: Number of decimals for the object
* format_use_thou: Use thousands separator for the object
* format_dec: Decimal separator for the object
* format_thou: Thousands separator for the object
* base_color: Base color (hex) of the object
* auxiliary
    - handle: the internal handle of the object in the Qlik Sense Engine API; can be used to access the measure via the `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the measure
    - parent: AppChildren object; you can access the App class object like this `ms.parent.parent`
    - created_date: creation date of the measure, as stored in Qlik Sense
    - modified_date: date of the last modification of the measure, as stored in Qlik Sense

#### Measure.copy()
Creates a copy of the master measure in another app

Args: target_app (App): The target app, where the measure will be copied
Returns: str: ID of the measure created if successful, None otherwise

#### Measure.update()
Updates the measure on the Qlik Sense Server

Args: 
* definition (str, optional): The definition of the measure
* description (str, optional): the description of the measure
* label (str, optional): the label of the measure, as it appears in charts
* label_expression (str, optional): the label expression of the measure
* format_type (str, optional): Format type of the object to be created. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec (int, optional): Number of decimals for the object to be created. Defaults to 10.
* format_use_thou (int, optional): Use thousands separator for the object to be created. Defaults to 0.
* format_dec (str, optional): Decimal separator for the object to be created. Defaults to ','.
* format_thou (str, optional): Thousands separator for the object to be created. Defaults to ''.
* base_color (str, optional): Base color (hex) of the object to be created. Defaults to None.

Returns: 
    True if the measure was updated successfully, False otherwise

```python
ms = app.measures['MyMeasure']
ms.update(definition = 'sum(Sales)', label = 'Total Sales', format_type = 'F')
app.save()
```

#### Measure.delete()
Deletes the measure from the Qlik Sense Server

Returns:
    True if the measure was deleted successfully, False otherwise

```python
ms = app.measures['MyMeasure']
ms.delete()
app.save()
```

#### Measure.rename()
Renames the measure on the Qlik Sense Server.

Returns:
    True if the measure was renamed successfully, False otherwise

```python
ms = app.measures['MyMeasure']
ms.rename('MyMeasureNewName')
app.save()
```

#### Measure.get_layout()
Returns the json layout of the measure; a shortcut to the GetLayout method of the Engine API

```python
ms.get_layout()
```

#### Measure.get_properties()
Returns the json properties of the measure; a shortcut to the GetProperties method of the Engine API

```python
ms.get_properties()
```

### Dimension class
The class represents master dimensions of the application and is a member of the App.dimensions collection. You can access a specific dimension by its name or iterate through them. Note that hierarchical dimensions are not yet supported."

```python
dim = app.dimensions['MyDimension']
print(dim.definition)

for dim in app.dimensions:
    if dim.definition == '[Customer]': dim.update(name = 'Customer_dimension')
```

#### Dimension properties
* name: the name of the dimension you generally use in the Qlik Sense interface
* definition: the formula behind the dimension
* label: the label of the dimension, as it appears in charts
* base_color: Base color (hex) of the object
* auxiliary
    - handle: the internal handle of the object in the Qlik Sense Engine API; can be used to access the dimension via the `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the dimension
    - parent: AppChildren object; you can access the App class object like this `dim.parent.parent`
    - created_date: creation date of the dimension, as stored in Qlik Sense
    - modified_date: date of the last modification of the dimension, as stored in Qlik Sense

#### Dimension.copy()
Creates a copy of the master dimension in another app

Args: target_app (App): The target app, where the dimension will be copied
Returns: str: ID of the dimension created if successful, None otherwise

#### Dimension.update()
Updates the dimension on the Qlik Sense Server

Args: 
* definition (str, optional): The definition of the dimension
* label (str, optional): the label of the dimension, as it appears in charts
* base_color (str, optional): Base color (hex) of the object to be created. Defaults to None.

Returns: 
    True if the dimension was updated successfully, False otherwise

```python
dim = app.dimensions['MyDimension']
dim.update(definition = 'Customer', label = 'Customer_dimension')
app.save()
```

#### Dimension.delete()
Deletes the dimension from the Qlik Sense Server

Returns:
    True if the dimension was deleted successfully, False otherwise

```python
dim = app.dimensions['MyDimension']
dim.delete()
app.save()
```

#### Dimension.rename()
Renames the dimension on the Qlik Sense Server.

Returns:
    True if the dimension was renamed succesfully, False otherwise

```python
dim = app.dimensions['MyDimension']
dim.rename('MyDimensionNewName')
app.save()
```

#### Dimension.get_layout()
Returns the json layout of the dimension; a shortcut to the GetLayout method of the Engine API

```python
dim.get_layout()
```

### Sheet class
The class represents the sheets of the application and is a member of the App.sheets collection. You can access objects on the sheets, such as charts and tables, via the Sheet class object.

```python
for sh in app.sheets:
    print(sh.name)
```

#### Sheet properties
* name: that's the name of the sheet
* description: the description of the sheet
* auxiliary
    - handle: the internal handle of the object in Qlik Sense Engine API; can be used to access the sheet via the `query()` function
    - app_handle: the handle of the parent App object
    - id: Qlik Sense internal id of the sheet
    - parent: AppChildren object; you can access the App class object like this `ms.parent.parent`
    - created_date: creation date of the sheet, as stored in Qlik Sense
    - modified_date: date of the last modification of the sheet, as stored in Qlik Sense
    - published: True if the sheet is published, False if not
    - approved: True if the sheet is approved, False if not
    - owner_id: GUID of the owner of the sheet
    - owner_name: name of the owner of the sheet

#### Sheet.copy()
Creates a copy of the sheet in another app

Args: 
* target_app (App): The target app, where the sheet will be copied
* master_match (str): 'name' by default: master measures and dimensions in the new object are matched by name. If 'id', they are matched by id.
Returns: str: ID of the sheet created if successful, None otherwise

```python
source_app = qsea.App(conn, 'Source AppName')
target_app = qsea.App(conn, 'Target AppName')
source_app.load()
target_app.load()

source_sh = source_app.sheets['SheetToCopy']
source_sh.copy(target_app = target_app)
```

Note: Some objects, not accessible via API (such as buttons) are not copied. Copying of conatainers and filterpanes is not supported. Master objects can be copied correctly only if they have 1-1 correspondence between the source and target apps and have the same IDs. It can be used as a workaround for the filterpane copy problem in some cases.

#### Sheet.load()
Loads objects from the sheet in a Qlik Sense application into a Sheet class object

```python
sh = App.sheets['MySheet']
sh.load()

for obj in sh.objects:
    print(obj.type)
```

#### Sheet.clear()
Clears all objects from the sheet in a Qlik Sense application

#### Sheet.get_layout()
Returns the json layout of the sheet; a shortcut to the GetLayout method of the Engine API

```python
sh.get_layout()
```


### Field class
The class represents the fields of the application and is a member of the App.fields collection. You can only use the class for information purposes; no changes can be made with fields via QSEA.

```python
for fld in app.fields:
    print(field.table_name, field.name)
```

#### Field properties
* name: name of the field, as it appears in the model
* table_name: name of the table, containing the field
* information_density, non_nulls, rows_count, subset_ratio, distinct_values_count, present_distinct_values, key_type, tags: properties of the fields as they can be found in the data model
* auxiliary
    - handle: internal handle of the field object
    - app_handle: handle of the parent App object

### Bookmark class
The class represents the bookmarks of the application and is a member of the App.bookmarks collection. You can only use the class for information purposes; no changes can be made with bookmarks via QSEA.

```python
for bm in app.bookmarks:
    print(bm.name)
```

#### Bookmark properties
* name: name of the bookmark
* owner_id: GUID of the owner of the bookmark
* owner_user_id: user id of the owner of the bookmark
* owner_name: name of the owner of the bookmark
* description: description of the bookmark
* state_data: selection properties of the bookmark in JSON format; unfortionately, the whole list of selections can not be retrieved correctly
* auxiliary
    - handle: internal handle of the bookmark object
    - app_handle: handle of the parent App object
    - id: Qlik Sense internal id of the bookmark
    - parent: AppChildren object; you can access the App class object like this `ms.parent.parent`
    - created_date: creation date of the bookmark, as stored in Qlik Sense
    - modified_date: date of the last modification of the bookmark, as stored in Qlik Sense
    - published: True if the bookmark is published, False if not
    - approved: True if the bookmark is approved, False if not




### Object class 
The class represents the objects on the sheet, such as charts and tables, and is a member of the SheetChildren collection.

#### Object properties
* type: type of the object, such as 'piechart' or 'pivot-table'
* col, row, colspan, rowspan, bounds_y, bounds_x, bounds_width, bounds_height: parameters referring to the location of an object on the sheet
* auxiliary
    - handle: the internal handle of the object in the Qlik Sense Engine API; can be used to access the object via the `query()` function
    - sheet_handle: handle of the parent sheet
    - sheet: the Sheet object, on which the object itself is located
    - id: Qlik Sense internal id of the object
    - parent: SheetChildren object

#### Object.export_data()
Performs data export of an object (such as a table or chart) to an xslx or csv file.

Args: 
* file_type (str, optional): 'xlsx' or 'csv', 'xlsx' by default
        
Returns: the path to the downloaded file in case of success, None if failed

#### Object.copy()
Creates a copy of the object in the specified sheet of another app

Args: 
* target_app (App): The target app, where the sheet will be copied
* target_sheet (Sheet): The target sheet, where the object will be copied
* col (int, optional): The column number of the new object, None by default (the column of the source object is used)
* row (int, optional): The row number of the new object, None by default (the row of the source object is used)
* colspan (int, optional): The number of columns occupied by the new object, None by default (the colspan of the source object is used)
* rowspan (int, optional): The number of rows occupied by the new object, None by default (the rowspan of the source object is used)
* master_match (str): 'name' by default: master measures and dimensions in the new object are matched by name. If 'id', they are matched by id.
Returns: str: ID of the sheet created if successful, None otherwise

```python
source_object.copy(target_app, target_sheet)
```

#### Object.load()
Loads measures and dimensions of the object in a Qlik Sense application into an Object class instance.

```python
sh = App.sheets['MySheet']
sh.load()

for obj in sh.objects:
    if obj.type == 'piechart': 
        obj.load()
        print(obj.dimensions.count)
```

#### Object.get_layout()
Returns the json layout of the object; a shortcut to the GetLayout method of the Engine API

```python
obj.get_layout()
```

### ObjectChildren class
The class contains collections of measures and dimensions in the object on the sheet:
* `object.measures`: a collection of ObjectMeasure class objects, representing the measures in the object on the sheet
* `object.dimensions`: a collection of ObjectDimension class objects, representing the dimensions in the object on the sheet
* `object.subitems`: a collection of Object class objects, representing the subitems of filterpane and container type objects

You can access the main information in pandas DataFrame via `.df`:
```python
App.sheets['MySheet'].objects['object_id'].measures.df
```

Adding measures and dimensions to app objects is not supported yet.


### ObjectMeasure class
This class represents measures of the object on the sheet and is a member of the object.measures collection. Since there may be no specific name for the measure in the object, the internal Qlik ID is used instead of the name. Thus, you can either iterate through measures or call them by the internal Qlik ID:
```python
ms = obj.measures['measure_id']
print(ms.definition)

for ms in obj.measures:
    if ms.definition == 'sum(Sales)': ms.update(definition = 'sum(Incomes)')
```

#### ObjectMeasure properties
* name: internal Qlik id of the measure
* definition: the formula behind the measure
* label: the label of the measure, as it appears in the charts
* label_expression: the label expression of the measure
* calc_condition: calculation condition for the measure
* library_id: if a master measure is used, this refers to its ID
* format_type: Format type of the object
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_ndec: Number of decimals of the object
* format_use_thou: Use thousands separator for the object
* format_dec: Decimal separator for the object
* format_thou: Thousands separator for the object
* auxiliary
    - app_handle: the handle of the parent App object
    - parent: ObjectChildren object
    - object: you can access the Object class object like this `ms.object`
    

#### ObjectMeasure.update()
Updates the measure in the object on the sheet.

Args: 
* definition (str, optional): The definition of the measure
* label (str, optional): the new label of the measure, as it appears in charts
* label_expression (str, optional): the label expression of the measure
* calc_condition (str, optional): calculation condition for the measure
* library_id (str, optional): id of the master measure
* format_type (str, optional): Format type of the object. Defaults to 'U'.
    - 'U' for auto
    - 'F' for number
    - 'M' for money
    - 'D' for date
    - 'IV' for duration
    - 'R' for other
* format_use_thou (int, optional): Use thousands separator for the object. Defaults to 0.
* format_dec (str, optional): Decimal separator for the object. Defaults to ','.
* format_thou (str, optional): Thousands separator for the object. Defaults to ''.

Returns: 
    True if the measure was updated successfully, False otherwise

```python
ms = obj.measures['measure_id']
ms.update(definition = 'sum(Sales)', label = 'Total Sales', format_type = 'F')
app.save()
```

#### ObjectMeasure.delete()
Deletes the measure from the object on the sheet

Returns:
    True if the measure was deleted successfully, False otherwise

```python
ms = obj.measures['measure_id']
ms.delete()
app.save()
```

### ObjectDimension class
This class represents dimensions of the object on the sheet and is a member of the object.dimensions collection. Since there may be no specific name for the dimension in the object, the internal Qlik ID is used instead of the name. Thus, you can either iterate through dimensions or call them by the internal Qlik ID:
```python
dim = obj.measures['dimension_id']
print(dim.definition)

for dim in obj.dimensions:
    if dim.definition == '[Customer]': dim.update(definition = '[Supplier]')
```

Note that hierarchical dimensions are not supported yet.

#### ObjectDimension properties
* name: internal Qlik id of the dimension
* definition: the formula behind the dimension
* label: the label of the dimension, as it appears in the charts
* auxiliary
    - app_handle: the handle of the parent App object
    - parent: ObjectChildren object
    - object: you can access the Object class object like this `dim.object`

#### ObjectDimension.update()
Updates the dimension in the object on the sheet

Args: 
* definition (str, optional): the definition of the dimension
* label (str, optional): the label of the dimension, as it appears in charts
* calc_condition (str, optional): calculation condition for the dimension

Returns: 
    True if the dimension was updated successfully, False otherwise

```python
dim = obj.dimensions['dimension_id']
dim.update(definition = 'Customer', label = 'Customer_dimension')
app.save()
```

#### ObjectDimension.delete()
Deletes the dimension from the Qlik Sense Server

Returns:
    True if the dimension was deleted successfully, False otherwise

```python
dim = app.dimensions['dimension_id']
dim.delete()
app.save()
```

## Roadmap
* support for master objects in the app
* support for hierarchical dimensions
* support for master item tags
* support for adding dimensions and measures to the object


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
