import React from 'react';
import ReactDOM from 'react-dom';

/*
The SideBar element defines the floating panel on the right side of the screen that
appears and dissapears in order to edit lines.
*/
class SideBar extends React.Component {
    render() {
        return (
            <div className = "side-bar">
                This is the sidebar edit panel. It is floating relative to the viewport.
            </div>
        )
    }
}

export default SideBar