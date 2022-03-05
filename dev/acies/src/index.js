import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


/* 
The ToolBar element defines the bar on the bottom of the screen and contains tool icon buttons and time controls
*/
class ToolBar extends React.Component {
    render() {
        return (
            <div className = "tool-bar">
                This is the toolbar. It is floating relative to the viewport.
            </div>
        );
    }
}

/*
The EditPanel element defines the floating panel on the right side of the screen that
appears and dissapears in order to edit lines.
*/
class EditPanel extends React.Component {
    render() {
        return (
            <div className = "edit-panel">
                This is the edit panel. It is floating relative to the viewport.
            </div>
        )
    }
}


/*
This is the main element of the app and contains the high-level layout of all other components
*/
class App extends React.Component {
  render() {
    return (
      <div className="app">
        <div className="grid">
            TODO: the grid will show up here as a canvas item
        </div>
        <ToolBar />
        <EditPanel />
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
