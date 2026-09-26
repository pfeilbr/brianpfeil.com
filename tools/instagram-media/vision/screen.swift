// Screens photos for the Google Photos picker with Apple's on-device Vision
// framework: nothing leaves the Mac.
//
//   vision-screen a.jpg b.jpg ...   ->  one JSON object per line on stdout
//
// For each image it reports how many people are in it (faces and bodies,
// counted separately, ignoring specks too small to be anyone), every piece of
// readable text, Vision's aesthetics score, whether Vision thinks the photo is
// a "utility" shot (receipt, screenshot, document), and the top scene labels.
// Policy — what counts as too many people or too much text — is decided in
// Python (igmedia/screen.py), not here, so it can be tested.

import Foundation
import Vision
import ImageIO

struct Result: Codable {
    var path: String
    var ok: Bool
    var error: String?
    var faces: Int = 0
    var faceAreas: [Double] = []
    var humans: Int = 0
    var humanAreas: [Double] = []
    var upperBodies: [Double] = []
    var persons: Int = 0          // separate people found by segmentation
    var personAreas: [Double] = []
    var text: [String] = []
    var aesthetics: Double?
    var utility: Bool?
    var labels: [String: Double] = [:]
}

func area(_ r: CGRect) -> Double { Double(r.width * r.height) }

/// Fraction of a mask's pixels that are set (the mask is a one-channel float buffer).
func coverage(_ buf: CVPixelBuffer) -> Double {
    CVPixelBufferLockBaseAddress(buf, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(buf, .readOnly) }
    let w = CVPixelBufferGetWidth(buf), h = CVPixelBufferGetHeight(buf)
    let row = CVPixelBufferGetBytesPerRow(buf)
    guard let base = CVPixelBufferGetBaseAddress(buf) else { return 0 }
    var on = 0
    for y in stride(from: 0, to: h, by: 2) {
        let p = base.advanced(by: y * row).assumingMemoryBound(to: Float32.self)
        for x in stride(from: 0, to: w, by: 2) where p[x] > 0.5 { on += 1 }
    }
    return Double(on) / Double(((w + 1) / 2) * ((h + 1) / 2))
}

func screen(_ path: String) -> Result {
    var out = Result(path: path, ok: false)
    let url = URL(fileURLWithPath: path)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
        out.error = "unreadable"
        return out
    }
    let faces = VNDetectFaceRectanglesRequest()
    let humans = VNDetectHumanRectanglesRequest()
    humans.upperBodyOnly = false
    // Upper bodies as well as whole ones: a chairlift selfie is two heads and
    // shoulders, which the whole-body detector tends to merge into one.
    let upper = VNDetectHumanRectanglesRequest()
    upper.upperBodyOnly = true
    // Segmentation separates people even when their faces are covered by
    // goggles and a balaclava, which defeats the face detector.
    let instances = VNGeneratePersonInstanceMaskRequest()
    let text = VNRecognizeTextRequest()
    text.recognitionLevel = .accurate
    text.usesLanguageCorrection = false
    let classify = VNClassifyImageRequest()
    let aesthetics = VNCalculateImageAestheticsScoresRequest()

    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    do {
        try handler.perform([faces, humans, upper, instances, text, classify, aesthetics])
    } catch {
        out.error = "\(error)"
        return out
    }
    let f = faces.results ?? []
    out.faces = f.count
    out.faceAreas = f.map { area($0.boundingBox) }
    let h = (humans.results ?? []).filter { $0.confidence > 0.5 }
    out.humans = h.count
    out.humanAreas = h.map { area($0.boundingBox) }
    out.upperBodies = (upper.results ?? []).filter { $0.confidence > 0.5 }.map { area($0.boundingBox) }
    if let mask = instances.results?.first {
        out.persons = mask.allInstances.count
        // Share of the frame each person covers, so a speck far away can be ignored.
        for i in mask.allInstances {
            if let m = try? mask.generateMask(forInstances: IndexSet(integer: i)) {
                out.personAreas.append(coverage(m))
            }
        }
    }
    out.text = (text.results ?? []).compactMap { obs in
        guard let top = obs.topCandidates(1).first, top.confidence >= 0.5 else { return nil }
        return top.string
    }
    if let a = aesthetics.results?.first {
        out.aesthetics = Double(a.overallScore)
        out.utility = a.isUtility
    }
    for c in (classify.results ?? []).prefix(40) where c.confidence >= 0.15 {
        out.labels[c.identifier] = (Double(c.confidence) * 1000).rounded() / 1000
    }
    out.ok = true
    return out
}

let enc = JSONEncoder()
enc.outputFormatting = [.sortedKeys]
for path in CommandLine.arguments.dropFirst() {
    let r = autoreleasepool { screen(path) }
    if let data = try? enc.encode(r), let line = String(data: data, encoding: .utf8) {
        print(line)
        fflush(stdout)
    }
}
