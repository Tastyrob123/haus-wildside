// Freisteller mit Apple Vision (lokal, kostenlos): swift freistellen.swift <eingang> <ausgang.png> [instanz-nummern, kommagetrennt]
import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins
import AppKit

let a = CommandLine.arguments
let url = URL(fileURLWithPath: a[1])
let aus = URL(fileURLWithPath: a[2])
guard let ci = CIImage(contentsOf: url) else { print("kein Bild"); exit(1) }
let handler = VNImageRequestHandler(ciImage: ci)
let req = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let r = req.results?.first else { print("nichts gefunden"); exit(2) }
print("Instanzen:", r.allInstances.map { $0 })
var wahl = r.allInstances
if a.count > 3 { wahl = IndexSet(a[3].split(separator: ",").compactMap { Int($0) }) }
let buf = try r.generateMaskedImage(ofInstances: wahl, from: handler, croppedToInstancesExtent: false)
let out = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
try ctx.writePNGRepresentation(of: out, to: aus, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
print("ok", out.extent)
