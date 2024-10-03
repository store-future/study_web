import React,{useState , useEffect} from 'react';
import axios from 'axios'


export default function Todos() {

  const [tasks , setTasks] = useState([]);
  const [inputValue , setInputValue] = useState('')

  //fetching value
  useEffect( ()=>{fetchTasks();} , []);

  const fetchTasks = async () =>{
      try{
        const response = await axios.get('http://127.0.0.1:8000/api/TodoList');
        setTasks(response.data)
      }
      catch(error){
        console.log('error' , error);
      }
  }

  // Add tasks
  const addTask = async () =>{
        try{
          if (inputValue.trim() !== ''){
            const response = await axios.post('http://127.0.0.1:8000/api/TodoList/add',{title:inputValue , completed:false });
            setTasks([...tasks , response.data]);   // adding two list 
            setInputValue('');
          }
        }
        catch(error){
          console.log('error',error)
        }
  }

  

  return (
    <div className="container">
      <div className="todo-app">
        <div className="app-title">
          <h2>To-do app</h2>
          <i className="fa-solid fa-book-bookmark"></i>
        </div>
        <div className="row">
          <input type="text" id="input-box" 
              placeholder="add your tasks" 
              value = {inputValue} 
              onChange={ (e) => setInputValue(e.target.value)} 
          />
          <button onClick={addTask}>Add</button>
        </div>
        <ul id="list-container">
          { tasks.map((item) => 
            (<li key={item.id}> {item.title} </li>) 
          )}
        </ul>
      </div>
    </div>
  );
}

