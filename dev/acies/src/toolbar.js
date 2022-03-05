import React from 'react';
import ReactDOM from 'react-dom';

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

export default ToolBar