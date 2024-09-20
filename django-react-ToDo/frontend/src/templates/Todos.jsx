export default function Todos() {
  return (
    <div className="container">
      <div className="todo-app">
        <div className="app-title">
          <h2>To-do app</h2>
          <i className="fa-solid fa-book-bookmark"></i>
        </div>
        <div className="row">
          <input type="text" id="input-box" placeholder="add your tasks" />
          <button>Add</button>
        </div>
        <ul id="list-container"></ul>
      </div>
    </div>
  );
}
