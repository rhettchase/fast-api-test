import './App.css';
import { Provider } from 'react-redux';
import store from './store';
import DynamicForm from './DynamicForm';

function App() {
  return (
    <div className='App'>
      <Provider store={store}>
        <div className='App'>
          <h1>Dynamic Form Demo</h1>
          <DynamicForm />
        </div>
      </Provider>
    </div>
  );
}

export default App;
