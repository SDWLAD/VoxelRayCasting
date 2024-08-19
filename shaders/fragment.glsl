#version 440 
layout (location = 0) out vec4 fragColor;

uniform vec2 u_resolution;
uniform vec3 u_position;
uniform vec2 u_mouse;
uniform sampler2D u_skybox;
uniform sampler3D u_voxel_data;

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
    if (p.x < 0 || p.y < 0 || p.z < 0 || p.x >= 64 || p.y >= 64 || p.z >= 64) {
        return false;
    }
    float voxel = texture(u_voxel_data, vec3(p) / 64.0).r;
    if (voxel != 0.0)
        return true;
}

vec3 getSky(vec3 rd) {
    vec2 uv = vec2(atan(rd.z, rd.x) / 3.14159265, -rd.y);
	uv = uv*0.5 + 0.5;
    vec3 col = texture(u_skybox, uv).rgb;
    return col;
}

vec3 lighting(vec3 norm, vec3 rd, vec3 col) {
    vec3 lightDir = normalize(vec3(0.3, 1, -0.5));
    float diffuseAttn = max(dot(norm, lightDir), 0.0);
    
    return col*(diffuseAttn);
}

Hit intersect(Ray ray) {
    vec3 pos = floor(ray.origin);
    vec3 step = sign(ray.direction);
    vec3 invDir = 1.0 / ray.direction;
    vec3 tDelta = abs(invDir);
    vec3 fr = fract(ray.origin);

    float tMaxX = tDelta.x * ((step.x > 0.0) ? (1.0 - fr.x) : fr.x);
    float tMaxY = tDelta.y * ((step.y > 0.0) ? (1.0 - fr.y) : fr.y);
    float tMaxZ = tDelta.z * ((step.z > 0.0) ? (1.0 - fr.z) : fr.z);

    vec3 norm;
    ivec3 iPos = ivec3(pos);  // Перетворення в ціле число для getVoxel

    const int maxTrace = 100;
    for (int i = 0; i < maxTrace; i++) {
        if (getVoxel(iPos)) {
            return Hit(length(pos - ray.origin), norm);
        }

        if (tMaxX < tMaxY && tMaxX < tMaxZ) {
            tMaxX += tDelta.x;
            iPos.x += int(step.x);  // Використання цілих чисел для коректного індексу
            norm = vec3(-step.x, 0.0, 0.0);
        } else if (tMaxY < tMaxZ) {
            tMaxY += tDelta.y;
            iPos.y += int(step.y);
            norm = vec3(0.0, -step.y, 0.0);
        } else {
            tMaxZ += tDelta.z;
            iPos.z += int(step.z);
            norm = vec3(0.0, 0.0, -step.z);
        }
    }

    return Hit(-1.0, vec3(0.0));
}


vec3 render(Ray ray){
    vec3 col = getSky(ray.direction);
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
