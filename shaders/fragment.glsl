#version 330 core
layout (location = 0) out vec4 fragColor;

uniform vec2 u_resolution;
uniform sampler3D u_world;
uniform vec3 u_position;
uniform vec2 u_mouse;

mat2 rot(float a) {
    float s = sin(a);
    float c = cos(a);
    return mat2(c, -s, s, c);
}

struct Ray{
    vec3 origin;
    vec3 direction;
};

struct Hit{
    float distance;
    vec3 normal;
};

struct Material{
    vec3 color;
};

bool getVoxel(ivec3 p) {
    return (length(p) < 15);
}

vec3 lighting(vec3 norm, vec3 rd, vec3 col) {
    vec3 lightDir = normalize(vec3(-1.0, 3.0, -1.0));
    float diffuseAttn = max(dot(norm, lightDir), 0.0);
    vec3 light = vec3(1.0,0.9,0.9);
    
    vec3 ambient = vec3(0.2, 0.2, 0.3);
    
    vec3 reflected = reflect(rd, norm);
    float specularAttn = max(dot(reflected, lightDir), 0.0);
    
    return col*(diffuseAttn*light*1.0 + specularAttn*light*0.6 + ambient);
}

Hit intersect(Ray ray) {
    vec3 pos = floor(ray.origin);
    
    vec3 step = sign(ray.direction);
    vec3 tDelta = step / ray.direction;

    
    float tMaxX, tMaxY, tMaxZ;
    
    vec3 fr = fract(ray.origin);
    
    tMaxX = tDelta.x * ((ray.direction.x>0.0) ? (1.0 - fr.x) : fr.x);
    tMaxY = tDelta.y * ((ray.direction.y>0.0) ? (1.0 - fr.y) : fr.y);
    tMaxZ = tDelta.z * ((ray.direction.z>0.0) ? (1.0 - fr.z) : fr.z);

    vec3 norm;
    const int maxTrace = 100;
    
    for (int i = 0; i < maxTrace; i++) {
        if (getVoxel(ivec3(pos))) {
            return Hit(length(pos-ray.origin), norm);
        }

        if (tMaxX < tMaxY) {
            if (tMaxZ < tMaxX) {
                tMaxZ += tDelta.z;
                pos.z += step.z;
                norm = vec3(0, 0,-step.z);
            } else {
                tMaxX += tDelta.x;
            	pos.x += step.x;
                norm = vec3(-step.x, 0, 0);
            }
        } else {
            if (tMaxZ < tMaxY) {
                tMaxZ += tDelta.z;
                pos.z += step.z;
                norm = vec3(0, 0, -step.z);
            } else {
            	tMaxY += tDelta.y;
            	pos.y += step.y;
                norm = vec3(0, -step.y, 0);
            }
        }
    }

 	return Hit(-1., vec3(0.));
}

vec3 render(Ray ray){
    vec3 col = vec3(0);
    Hit hit = intersect(ray);

    if (hit.distance >= 0)
        col = lighting(hit.normal, ray.direction, vec3(1.));

    return col;
}

void main(){    
    vec2 uv = (2.0 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y;

    Ray ray = Ray(u_position, normalize(vec3(uv, 1.0)));
    ray.direction.zy *= rot(-u_mouse.y);
    ray.direction.zx *= rot(u_mouse.x);
    vec3 color = render(ray);

    fragColor = vec4(color, 1);
}