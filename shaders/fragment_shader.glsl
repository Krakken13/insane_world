#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D screenTexture;

void main() {
    vec2 offset = vec2(1.0 / 320.0, 1.0 / 180.0);
    vec3 result = texture(screenTexture, TexCoord).rgb * 0.4;

    result += texture(screenTexture, TexCoord + vec2(offset.x, 0.0)).rgb * 0.15;
    result += texture(screenTexture, TexCoord - vec2(offset.x, 0.0)).rgb * 0.15;
    result += texture(screenTexture, TexCoord + vec2(0.0, offset.y)).rgb * 0.15;
    result += texture(screenTexture, TexCoord - vec2(0.0, offset.y)).rgb * 0.15;

    FragColor = vec4(result, 1.0);
}