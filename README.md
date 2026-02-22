# Geographic-Centre
The Centre of N Points was my A-Level Computer Science coursework project, a weave of Mathematics and Computing to explore a problem that fascinated me. Given $n$ points in some space $S$, what is the point in $S$ that is equidistant from from all those points. Right now that seems vague and poorly defined, and thats because it is ! The original problem was spurred on from an issue me and my family were having: we are scattered across the UK, where would be a location to meet such that each party would have to travel an equal distance to travel to arrive at that location. Furthermore, what would be a location that would be an equal distance to travel whilst also minimizing the total distance that all parties have to travel. At the time, I was learning Djikstra's algorithm and A*; as well as learning the basics of 3D geometry and calculus. Thus, I pursued this problem for my A-Level project.<br>

This involved a deep exploration into mathematics and optimisation. The original project was created with PyQt5 for the interface; but later I engineered this to work on my website in Python (for a Flask server backend) and then in raw JavaScript. These are all included, with the original in the PyQT directory, the flask implementation in the Flask directory and the JavaScript implementation in the JS directory. You will see a general improvement in understanding and programming, as PyQT was done as an A-Level Student, Flask was done as a 2nd Year Graduate, and JS was done post graduation (currently incomplete). While the PyQT and Flask implementations likely won't fully work, lacking a server or API keys, the JavaScript implementation is fully complete and should be able to be run locally without issue. You can run this like so:<br>
1. Clone the project 
```
git clone https://github.com/Illuminarchie66/Geographic-Centre.git
```
2. Navigate into the correct folder and run a local server: 
```
cd JS
python -m http.server
```
3. Then go and visit the associated page: `http://localhost:8000/`

You can read the design more thoroughly here: [Geographic Centre](https://www.archie-harrodine.com/projects/project?key=geographic-centre).