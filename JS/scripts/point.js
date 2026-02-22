import * as THREE from 'three';

class Polar {
    constructor({ degrees, radians, latitude, longitude } = {}) {
        if (degrees) {
            this.radians = degrees.clone().multiplyScalar(Math.PI / 180);
        } else if (radians) {
            this.radians = radians.clone();
        } else if (latitude !== undefined && longitude !== undefined) {
            this.radians = new THREE.Vector2(latitude, longitude)
                .multiplyScalar(Math.PI / 180);
        } else {
            throw new Error("No polar input.");
        }
    }

    get degrees() {
        return this.radians.clone().multiplyScalar(180 / Math.PI);
    }

    toString() {
        const d = this.degrees;
        return `(${d.x}, ${d.y})`;
    }
}


class Point {
    // R = 1

    static cartesianToRadians(v) {
        const lat = Math.asin(v.z);
        const lng = Math.atan2(v.y, v.x);
        return new THREE.Vector2(lat, lng);
    }

    static polarToCartesian(p) {
        const x = Math.cos(p.radians.x)*Math.cos(p.radians.y);
        const y = Math.cos(p.radians.x)*Math.sin(p.radians.y);
        const z = Math.sin(p.radians.x);
        return new THREE.Vector3(x,y,z);
    }

    constructor({
            cartesian, x, y, z, 
            polar, latitude, longitude,
            address
        } = {}) {
            
            if (address !== undefined) {
                this.address = address;
            }

            if (cartesian !== undefined) {
                this.cartesian = cartesian; 
                this.polar = new Polar({radians: Point.cartesianToRadians(this.cartesian)});
            } else if (x !== undefined && y !== undefined && z !== undefined) {
                this.cartesian = new THREE.Vector3(x,y,z);
                this.polar = new Polar({radians: Point.cartesianToRadians(this.cartesian)});
            } else if (polar !== undefined) {
                this.polar = polar;
                this.cartesian = Point.polarToCartesian(this.polar);
            } else if (latitude !== undefined && longitude !== undefined) {
                this.polar = new Polar({latitude: latitude, longitude: longitude});
                this.cartesian = Point.polarToCartesian(this.polar);
            }

    }

    setLatLng(latitude, longitude) {
        this.polar = new Polar({latitude: latitude, longitude: longitude});
        this.cartesian = Point.polarToCartesian(this.polar);
    }
}

export {Polar, Point};