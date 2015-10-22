#version 330

// Per frame data
uniform mat4 perspective;
uniform mat4 view;

// Per object data
uniform mat4 world;

// Per vertex data
in vec2 vinPosition;

void main(void)
{
    gl_Position =  perspective * view * world * vec4(vec3(vinPosition, 0.0), 1.0);
}

