import {settings} from './settings.js';
import {Polar, Point} from './point.js';
import {markers} from './map.js';
import * as THREE from 'three';

function calculate() {
    if (markers.length == 1) {
        console.log("1 point");
    } else if (markers.length == 2) {
         console.log("2 points");
    } else if (markers.length == 3) {
         console.log("3 points");
    } else if (markers.length > 3) {
         console.log("n points");
    }
}

function centre2(p1, p2) {
    const lat1 = p1.polar.radians.x;
    const lat2 = p2.polar.radians.x;
    const lng1 = p1.polar.radians.y;
    const lng2 = p2.polar.radians.y;

    const Bx = Math.cos(lat2) * Math.cos(lng2 - lng1);
    const By = Math.cos(lat2) * Math.sin(lng2 - lng1);

    const midlat = Math.atan2(
        Math.sin(lat1) + Math.sin(lat2),
        Math.sqrt(Math.pow(Math.cos(lat1) + Bx, 2) + Math.pow(By, 2))
    );
    const midlng = lng1 + Math.atan2(By, Math.cos(lat1) + Bx);

    return new Point({polar: new Polar({radians: new THREE.Vector2(midlat, midlng)})});
}

function createPerpendicular(p1, p2) {
    const plane = p1.cartesian.clone().cross(p2.cartesian);
    const centre = (p1.cartesian.clone().add(p2.cartesian)).multiplyScalar(0.5);
    const perpendicular = plane.clone().cross(centre);
    return perpendicular;
}

function centre3(p1,p2,p3) {
    const perp1 = createPerpendicular(p1, p2);
    const perp2 = createPerpendicular(p1, p3);
    const y_coef = -((perp1.x*perp2.z - perp1.z*perp2.x) / (perp1.y*perp2.z - perp1.z*perp2.y));
    const z_coef = -((perp1.x*perp2.y - perp1.y*perp2.x) / (perp1.z*perp2.y - perp1.y*perp2.z));
    const t = 1/Math.sqrt(1 + Math.pow(y_coef, 2) + Math.pow(z_coef, 2));
    return new Point({cartesian: new THREE.Vector3(t, t*y_coef, t*z_coef)});
}

function grad(c, V, K) {
    const n = V.length;
    const cross_product = new Float32Array(n);
    const dot_product = new Float32Array(n);
    const inverse_div = new Float32Array(n);
    const inverse_sum = new Float32Array(n);
    const arctan = new Float32Array(n);

    const s1 = new THREE.Vector3(0,0,0);
    const s2 = 0;
    const s3 = new THREE.Vector3(0,0,0);
    
    for (let i = 0; i < n; i++) {
        cross_product[i] = V[i].clone().cross(c).length();
        dot_product[i] = V[i].dot(c);
        arctan[i] = Math.atan2(cross_product[i], dot_product[i]);
        inverse_div[i] = dot_product[i] / cross_product[i];
        inverse_sum[i] = 1/(Math.pow(cross_product[i], 2) + Math.pow(dot_product[i], 2));

        const temp = (
            (
                c.clone().applyMatrix3(K[i])
            ).multiplyScalar(inverse_div[i])
        ).sub(
            V[i].clone().multiplyScalar(cross_product[i])
        ).multiplyScalar(inverse_sum[i])
        s1.add(temp.clone().multiplyScalar(arctan[i]));
        s2 += arctan[i];
        s3.add(temp);
    }

    return s1.clone().multiplyScalar(2/n).sub(s3.clone().multiplyScalar(2*s2/Math.sqrt(n)));
}

function centreN(points) {
    const n = points.length;
    
}

const p1 = new Point({latitude: -15, longitude: 0});
const p2 = new Point({latitude: 15, longitude: 0});
const p3 = new Point({latitude: 0, longitude: 14});

const c = centre3(p1, p2, p3);
console.log(c.polar.degrees);

document.getElementById("calculate-btn")
    .addEventListener("click", calculate);