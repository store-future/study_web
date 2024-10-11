import React,{useState , useEffect} from 'react';
import axios from 'axios'


export default function Todos() {

  const [tasks , setTasks] = useState([]);
  const [inputValue , setInputValue] = useState('')


  // Fetch value
  useEffect( ()=>{fetchTasks();} , []);

  const fetchTasks = async () =>{
      try{
        const response = await axios.get('http://127.0.0.1:8000/api/TodoList');
        setTasks(response.data)
        console.log(` Fetched data from database server ${JSON.stringify(response.data)}`);
      }
        catch(error){
        console.log('error' , error);
      }
  }


  // Add tasks
  const addTask = async () =>{
        try{
          if (inputValue.trim() !== ''){
            const response = await axios.post('http://127.0.0.1:8000/api/TodoList/add',{title:inputValue , status:false });
            setTasks([...tasks , response.data]);   // adding two list 
            setInputValue('');
          }
        }
        catch(error){
          console.log('error',error)
        }
  }

  
  // Update tasks
  const toggleCompleted = async (taskId) =>{
        try{
          const taskToUpdate = tasks.find(task => task.id ==taskId)
          console.log(` tasks element that will be update ${JSON.stringify(taskToUpdate)}`);
          
          if (taskToUpdate){
            const response = await axios.put(`http://127.0.0.1:8000/api/TodoList/${taskId}/update`,{status: !taskToUpdate.status });
            const updatedTasks = tasks.map(task => task.id ===taskId ?{ ...task, status :response.data.status} :task);
            setTasks(updatedTasks)
            console.log(` After updating new tasks list ${JSON.stringify(updatedTasks)}`);

          }
        }
        catch(error){
          console.log('error',error)
        }
  }


  // Delete task
  const deleteTask = async (taskId) =>{
    try{
      const taskToDelete = tasks.find(task => task.id ==taskId)
      console.log(` tasks that will be delete ${JSON.stringify(taskToDelete)}`);
      
      if (taskToDelete){
        await axios.delete(`http://127.0.0.1:8000/api/TodoList/${taskId}/delete`);
        const updatedTasks = tasks.filter(task => task.id !== taskId );
        setTasks(updatedTasks)
        console.log(` tasks list after delete ${JSON.stringify(updatedTasks)}`);
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
          { tasks.map( (item) => 
            (<li key={item.id} 
            
                 onClick={() => toggleCompleted(item.id)}  // Fix here
                 className = {item.status ? 'checked' : ''}> 
                 {item.status ? <del>{item.title} </del> :item.title}
                
                 <span
                 onClick={(e) => {
                   e.stopPropagation(); // Prevents triggering the parent <li> click event
                   deleteTask(item.id);
                 }}
               >X</span>
            </li> )
          )}
        </ul>
        <h1 onClick={(e) => { console.log(e); }}>Click me</h1>
      </div>
    </div>
  );
}

//<span onClick={ () => deleteTask(item.id)}>X</span>