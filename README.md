# ToDoList
This is a todo project in python for study. This app is simplicity and beauty.

## Installation
Please use git clone to your favorit folder.

```bash
gh repo clone robertos1232/ToDoList
```
I personally run this application on ubuntu 22.04 with python 3.7.

Before running this app, you should install few pip modules

```bash
#pip requirements
pip3 install kivy kivymd sqlalchemy pytest fastapi
# also from apt please install xclip and sqlite3
sudo apt-get install xclip
sudo apt install sqllite
```

After git clone please go to:

```bash
cd ToDoList/second_beta/done_i_guess/todo_app/
chmod +x main.py
./main.py
```

## Api
Our application also have api on port 5000. We are using fastapi :)
![Screenshot from 2023-06-05 21-13-23](https://github.com/robertos1232/ToDoList/assets/40420170/4ffbc8a2-a4a1-471e-958a-6c664d682697)


```bash
GET /lists

GET /lists/{list_id}

PUT /lists

PUT /lists/{list_id}

POST /lists/{list_id}/items/{item_id}

DELETE /lists/{list_id}/items/{item_id}


#Example
GET /lists
[{"id":1,"name":"test3"},{"id":2,"name":"test4"},{"id":3,"name":"test5"}]

GET /lists/{list_id}
[{"description":"t1","priority":0,"todolist_id":"1","done":false,"id":1},{"description":"t2","priority":3,"todolist_id":"1","done":false,"id":2},{"description":"t3","priority":2,"todolist_id":"1","done":false,"id":3}]


```





## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

[AppDemo.webm](https://github.com/robertos1232/ToDoList/assets/40420170/09815d7a-0b96-4c10-9b8f-e2ec2c9a76e6)
