import ROOT as r
r.gROOT.SetBatch(True)
clock = r.TStopwatch()
clock.Start()

r.gStyle.SetOptStat(0)
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle() 


def createRatio(h1, h2,col):
    h3 = h1.Clone("h3")
    h3.SetLineColor(col)
    h3.SetMarkerColor(col)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.0)
    h3.SetMaximum(2.20)
    # Set up plot for markers and errors
    #h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio (SM/aQGC)")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle("m (dilep) ")
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    return h3

def createCanvasPads():
    c = r.TCanvas("c", "canvas", 600, 700)
    # Upper histogram plot is pad1
    pad1 = r.TPad("pad1", "pad1", 0.0, 0.3, 1.0, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetLeftMargin(0.1)
    pad1.SetRightMargin(0.03)
    pad1.SetLogy(1)
    pad1.SetGridx()
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = r.TPad("pad2", "pad2", 0.0, 0.00, 1.0, 0.3)
    #pad2.SetLogy(1)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.25)
    pad2.SetLeftMargin(0.1)
    pad2.SetRightMargin(0.03)
    pad2.SetGridx()
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.Draw()

    return c, pad1, pad2

#canvas = r.TCanvas() 
#canvas.SetLogy(1)
#canvas.SetTickx(1)
#canvas.SetTicky(1) 
#canvas.SetGrid()

leg = r.TLegend(0.6,0.75,0.9,0.9)
#leg = r.TLegend(0.1,0.1,0.45,0.3)

# Read three fils and their tree
tfile_Mini = r.TFile("//afs/cern.ch/user/a/asahmed/work/GenSIMAnalyzer/CMSSW_8_0_11/src/GEN-SIM-analyzer/GenAnalyzer/aQGC_LHE_validation/MiniAod_2018v6_Comipled.root")
tfile_Nano = r.TFile("/afs/cern.ch/user/a/asahmed/work/GenSIMAnalyzer/CMSSW_8_0_11/src/GEN-SIM-analyzer/GenAnalyzer/aQGC_LHE_validation/nano_1.root")

tree_Mini = tfile_Mini.Get("otree")
tree_Nano = tfile_Nano.Get("Events")

# See which weights we are going to apply
for n, event in enumerate(tree_Nano):
	if n>1:
		break
	print "LHEReweightingWeight = ",event.LHEReweightingWeight[0],"\toriginalXWGTUP = ",event.LHEWeight_originalXWGTUP,"\taQGC Weight: = ",event.LHEWeight_originalXWGTUP*event.LHEReweightingWeight[0]
########################################
for n, event in enumerate(tree_Mini):
	print "Reading Histo: h_MiniAOD..."
	if n>100:
		break
	print "LHEWeights = ",event.LHEWeights[0]
# Define 3 histogram for three different samples
## Hist 1
print "Reading Histo: h_OnlyFT1_initialize..."
h_Mini = r.TH1F("h_Mini","",100,-5.0,5.0)
h_Mini.GetXaxis().SetTitle("FT0")
ylabel = "Events / %s GeV" % int(h_Mini.GetBinWidth(1))
h_Mini.GetYaxis().SetTitle(ylabel)
h_Mini.SetLineColor(1)
h_Mini.SetMarkerColor(1)
leg.AddEntry(h_Mini,"MiniAOD","lpe")
#leg.AddEntry(h_OnlyFT1_initialize,"Reweighted SM","lpe")
#h_aQGC = r.TH1F("aQGC","",20,0,5000)

## Hist 2
print "Reading Histo: h_aQGC..."
h_Nano = r.TH1F("h_Nano","",100,-5.0,5.0)
h_Nano.GetXaxis().SetTitle("FT0")
ylabel = "Events / %s GeV" % int(h_Nano.GetBinWidth(1))
h_Nano.GetYaxis().SetTitle(ylabel)
h_Nano.SetLineColor(2)
h_Nano.SetMarkerColor(2)
leg.AddEntry(h_Nano,"NanoAOD","lpe")
#leg.AddEntry(h_aQGC,"Reweighted SM","lpe")

## Hist 5

# Fill & Draw all 3 histogram from three different trees. Apply weight in aQGC sample only
#tree_OnlyFT1_initialize.Draw("LHE_MothInfo_mtWW>>h_OnlyFT1_initialize","(aqgcWeight[491])*(LHE_MothInfo_mjj>200 && LHELeptPt>20 && LHE_MothInfo_Iqrk1_pt > 20 && LHE_MothInfo_Iqrk0_pt > 20)")
print "reading tree : 1"
#tree_Mini.Draw("event.LHEWeights[0]>>h_Mini","","")
tree_Mini.Draw("gen_mjj>>h_Mini","","")
#tree_OnlyFT1_initialize.Draw("dilep_m>>h_OnlyFT1_initialize","59.0*0.2223*aqgcWeight[0]/(1.0)","")
#print "reading tree : 2"
print "reading tree : 5"
tree_Nano.Draw("LHEWeight_originalXWGTUP>>h_Nano","","")
#tree_Nano.Draw("LHEReweightingWeight[147]*LHEWeight_originalXWGTUP>>h_Nano","","")

# Normalize histogram with unity
#h_OnlyFT1_initialize.Scale(1.0/h_OnlyFT1_initialize.Integral())
#h_AllaQGCPar_initialize.Scale(1.0/h_AllaQGCPar_initialize.Integral())
#h_aQGC.Scale(1.0/h_aQGC.Integral())
#h_FT0_10e12.Scale(1.0/h_FT0_10e12.Integral())
#h_FT0_14e12.Scale(1.0/h_FT0_14e12.Integral())
#h_SM.Scale(1.0/h_SM.Integral())

h3 = createRatio(h_Mini,h_Nano,1)
#h4 = createRatio(h_SM,h_aQGC,2)
#h5 = createRatio(h_SM,h_aQGC,2)
#h6 = createRatio(h_SM,h_FT0_10e12,3)
#h7 = createRatio(h_SM,h_FT0_14e12,4)

canvas, pad1, pad2 = createCanvasPads()

#print "Integral h_OnlyFT1_initialize = ",h_OnlyFT1_initialize.Integral()
#print "Integral h_AllaQGCPar_initialize = ",h_AllaQGCPar_initialize.Integral()
#print "Integral h_SM = ",h_SM.Integral()

# Draw all hitogram using sames.
pad1.cd()
h_Mini.Draw()
h_Nano.Draw("same")
#h_aQGC.Draw("same")
#h_FT0_8e12.Draw("same")
#h_FT0_10e12.Draw("same")

leg.Draw()

pad2.cd()
h3.Draw("ep")
#h4.Draw("ep same")
l = r.TLine( 0, 1, 5000, 1 )
l.SetLineStyle(3)
l.Draw("same")

#canvas.Draw()
canvas.SaveAs("FT0.png")
#canvas.SaveAs("mt_plot_Comp_DifferentSM_Range5000_b250_log.pdf")

clock.Stop()

print 'Tree loop profiling stats:'
print 'Real Time used:', clock.RealTime()
print 'CPU Time used:', clock.CpuTime()
