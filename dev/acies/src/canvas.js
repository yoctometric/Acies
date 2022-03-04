/*
Heavily influenced by tutorial found here:
    Link: https://medium.com/@pdx.lucasm/canvas-with-react-js-32e133c05258
    Author: Lucas Miranda

This defines a react element wrapper for the HTML canvas element.
*/

import React, { useRef, useEffect } from 'react'


const Canvas = props => {
  
    // store draw from props, set up reference
    const { draw, ...rest } = props
    const canvasRef = useRef(null)
    
    // use effect hook. called by dependancies. See: https://www.reactjstutorials.com/react-basics/26/react-useeffect
    useEffect(() => {
        // when draw is changed, call draw
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')

        draw(context)
        
    }, [draw])
    
    return <canvas ref={canvasRef} {...rest}/>
  }
  

export default Canvas