

/*
The grid class contains data defining how the grid is to be rendered to the canvas

*/

class Grid {
    width; // num points in x axis
    height; // num points in y axis
    pointSpacing; // num units between each point
    pointSize; // radius of points
    pointArray; // 2D array of GridPoints
    
    constructor(width, height, pointSpacing, pointSize) {
        this.width = width;
        this.height = height;
        this.pointSpacing = pointSpacing; 
        this.pointSize = pointSize;

        // generate grid points 2d array
        let arr = new Array(width); // create empty array of w = width
        for (let i = 0; i < width; i++) {
            // populate with column arrays of length height
            let columnArray = new Array(height);

            // fill column with points
            for (let j = 0; j < height; j++) {
                let p = new GridPoint(i * pointSpacing, j * pointSpacing);
                arr[j] = p;
            }

            arr[i] = columnArray;
        }

        // finally, set point array
        this.pointArray = arr;
    }
    
    // the draw function returns a draw function to pass to the canvas class for rendering
    draw(ctx) {
        // return draw function
        const d = ctx => {
            console.log("calling grid draw");

            // setup fill color
            ctx.fillStyle = '#000000';

            // loop thru all points and draw
            for (let x = 0; x < this.pointArray.length; x++) {
                for (let y = 0; y < this.pointArray.length; y++) {
                    let gridPoint = this.pointArray[x][y];
                    console.log(gridPoint);
                    ctx.beginPath();
                    ctx.arc(gridPoint.x, gridPoint.y, this.pointSize, 0, 2*Math.PI);
                    ctx.fill();
                }
            }
        }

        return d;
    }
}

class GridPoint {
    x;
    y;
    constructor(x, y) {
        this.x = x;
        this.y = y;

        console.log("point at ", x, ", ", y);
    }
}


export default Grid