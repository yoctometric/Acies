import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// import custom classes
import Canvas from "./canvas"
import ToolBar from "./toolbar"
import SideBar from "./sidebar"
import Grid from "./grid"


// TODO: remove temp draw
/*
const draw = ctx => {
  ctx.fillStyle = '#000000'
  ctx.beginPath()
  ctx.arc(50, 100, 20, 0, 2*Math.PI)
  ctx.fill()
}*/



/*
This is the main element of the app and contains the high-level layout of all other components
*/
class App extends React.Component {

  render() {
    const grid = new Grid(10, 10, 10, 4);

    const draw = grid.draw()
    return (
      <div className='app'>
        <Canvas draw={draw} />
        <ToolBar />
        <SideBar />
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
