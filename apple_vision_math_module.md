# Apple Vision Math Module

## Purpose
The Apple Vision Math Module is a compact framework for handling spatial math in mixed-reality experiences (for example, on Apple Vision Pro). It provides a consistent way to represent position, orientation, scale, projection, and interaction geometry.

## Core coordinate spaces
1. **World space**: A stable reference frame for the room or environment.
2. **Device/head space**: Coordinates relative to the headset origin.
3. **View (camera) space**: Coordinates relative to the current eye or render camera.
4. **Clip/NDC space**: Normalized coordinates after projection.
5. **Screen space**: Pixel-based coordinates for final display and UI overlays.

A common transform chain is:

`p_screen = Viewport * Projection * View * Model * p_local`

## Fundamental math primitives
- **Vector2 / Vector3 / Vector4** for points and directions.
- **Matrix4x4** for affine transforms.
- **Quaternion** for robust 3D rotation and interpolation.
- **Pose** abstraction: `(translation, rotation)` pair.
- **Ray** for gaze, pointer, and hit testing.
- **Plane / AABB / OBB / Sphere** for collision and culling.

## Essential operations
- Compose transforms with matrix multiplication.
- Convert points between spaces using precomputed inverse matrices.
- Rotate vectors with quaternions to avoid gimbal lock.
- Normalize and orthogonalize basis vectors to maintain numerical stability.
- Use epsilon-aware comparisons for floating point equality.

## Example module API (conceptual)
```swift
struct Pose {
    var position: SIMD3<Float>
    var orientation: simd_quatf
}

enum Space {
    case local, world, view, screen
}

protocol VisionMathModule {
    func compose(_ a: Pose, _ b: Pose) -> Pose
    func inverse(_ pose: Pose) -> Pose
    func transform(point: SIMD3<Float>, by pose: Pose) -> SIMD3<Float>
    func convert(point: SIMD3<Float>, from: Space, to: Space) -> SIMD3<Float>
    func raycast(origin: SIMD3<Float>, direction: SIMD3<Float>, against plane: simd_float4) -> SIMD3<Float>?
}
```

## Projection and depth
- Prefer physically plausible projection parameters (near/far planes tuned to scene scale).
- Keep near plane as far as acceptable to improve depth precision.
- Use reversed-Z when the rendering stack supports it for better precision at distance.

## Interaction math
- **Gaze targeting**: Intersect gaze rays with scene geometry and sort by confidence and distance.
- **Pinch/manipulation**: Derive object delta transform from hand pose deltas.
- **Anchoring**: Keep virtual content stable by blending sensor updates with temporal smoothing.
- **Snapping**: Apply positional/angular thresholds in local object frames for predictable UX.

## Performance guidelines
- Cache derived matrices per frame.
- Batch transform operations with SIMD.
- Avoid repeated inversion; update inverse lazily when source transform changes.
- Keep hot paths allocation-free.

## Validation checklist
- Unit-test conversion consistency: `A -> B -> A` should return original values within epsilon.
- Verify handedness assumptions across imported assets and rendering pipeline.
- Run stress tests with extreme scales (tiny and very large coordinates).
- Record and replay head/hand traces to regression-test interaction math.

## Practical recommendation
Build the math layer as an engine-agnostic module first, then add thin adapters for RealityKit/ARKit data types. This keeps business logic portable while still integrating tightly with Apple’s spatial computing stack.
