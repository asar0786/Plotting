import ROOT as r
import argparse
r.gROOT.SetBatch(True)
clock = r.TStopwatch()
clock.Start()

r.gStyle.SetOptStat(0)
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle() 

#def getBasicParser():
#	parser = argparse.ArgumentParser()
#	parser.add_argument('-v', '--tree_var', type=str, required=False, default="LHE_MothInfo_mtWLep",
#			    help="Variable name in root tree")
#	return parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--tree_var", type=str, required=True, default="LHE_MothInfo_mtWLep", help="Variable name in root tree")
ap.add_argument("--xmin", type=float, required=False, default="0.0", help="minimum range of histogram")
ap.add_argument("--xmax", type=float, required=False, default="1000.0", help="maximum range of histogram")
ap.add_argument("--nbin", type=int, required=False, default="20", help="number of bins in histogramam")
args = ap.parse_args()
print args.tree_var
#print args['tree_var']
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
    x.SetTitle(args.tree_var+" (GeV)")
    #x.SetTitle("LHE_MothInfo_mtWLep (GeV)")
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

#leg = r.TLegend(0.6,0.65,0.9,0.9)
leg = r.TLegend(0.1,0.1,0.4,0.3)

# Read three fils and their tree
tfile_OnlyFT1_initialize = r.TFile("../GenSim_WminusToLNuWminusTo2JJJ_EWK_LO_aQGC_MJJ100PTJ10_2018_MiniAOD.root")
#tfile_AllaQGCPar_initialize = r.TFile("root:://cmseos.fnal.gov//eos/uscms/store/user/rasharma/LHE_GEN_Analyzer_Output/aQGC_WPlepWMhadJJ_EWK_LO_NPle1_RunCardChanged_InitilaizeAllaQGCPar_Pythia8CUEP8M1_13TeV_Madgraph.root")
tfile_SM = r.TFile("../GenSim_WminusToLNuWminusTo2JJJ_EWK_LO_SM_MJJ100PTJ10_2018_MiniAOD.root")

tree_OnlyFT1_initialize = tfile_OnlyFT1_initialize.Get("otree")
#tree_AllaQGCPar_initialize = tfile_AllaQGCPar_initialize.Get("otree")
tree_SM = tfile_SM.Get("otree")

# See which weights we are going to apply
for n, event in enumerate(tree_OnlyFT1_initialize):
	if n>1:
		break
	print "Weight Details for OnlyFT1_initialize: ID = ",event.LHE_MothInfo_mtWLep,"\tWeight = ",event.LHEWeights[181]
#for n, event in enumerate(tree_AllaQGCPar_initialize):
#	if n>0:
#		break
#	print "Weight Details for AllaQGCPar_initialize: ID = ",event.LHEWeightIDs[491],"\tWeight = ",event.LHEWeights[491]


# Define 3 histogram for three different samples
## Hist 1
print "Reading Histo: h_OnlyFT1_initialize..."
#h_OnlyFT1_initialize = r.TH1F("h_OnlyFT1_initialize","",20,args.xmin,args.xmax)
h_OnlyFT1_initialize = r.TH1F("h_OnlyFT1_initialize","",args.nbin,args.xmin,args.xmax)
h_OnlyFT1_initialize.GetXaxis().SetTitle("mT (WW) GeV")
ylabel = "Events / %s GeV" % int(h_OnlyFT1_initialize.GetBinWidth(1))
h_OnlyFT1_initialize.GetYaxis().SetTitle(ylabel)
h_OnlyFT1_initialize.SetLineColor(1)
h_OnlyFT1_initialize.SetMarkerColor(1)
leg.AddEntry(h_OnlyFT1_initialize,"Reweighted SM (FT0=6.25)","lpe")
#leg.AddEntry(h_OnlyFT1_initialize,"Reweighted SM","lpe")

## Hist 2
print "Reading Histo: h_aQGC_initialize..."
h_aQGC_initialize = r.TH1F("h_aQGC_initialize","",args.nbin,args.xmin,args.xmax)
h_aQGC_initialize.GetXaxis().SetTitle("mT (WW) GeV")
ylabel = "Events / %s GeV" % int(h_OnlyFT1_initialize.GetBinWidth(1))
h_aQGC_initialize.GetYaxis().SetTitle(ylabel)
h_aQGC_initialize.SetLineColor(2)
h_aQGC_initialize.SetMarkerColor(2)
leg.AddEntry(h_aQGC_initialize,"aQGC","lpe")
#leg.AddEntry(h_OnlyFT1_initialize,"Reweighted SM","lpe")

## Hist 3
#print "Reading Histo: h_FT0_14e12..."
#h_FT0_14e12 = r.TH1F("h_FT0_14e12","",20,0,1500)
#h_FT0_14e12.GetXaxis().SetTitle("mT (WW) GeV")
#ylabel = "Events / %s GeV" % int(h_FT0_14e12.GetBinWidth(1))
#h_FT0_14e12.GetYaxis().SetTitle(ylabel)
#h_FT0_14e12.SetLineColor(4)
#h_FT0_14e12.SetMarkerColor(4)
#leg.AddEntry(h_FT0_14e12,"Reweighted SM (FT0=14.0)","lpe")
#leg.AddEntry(h_FT0_14e12,"Reweighted SM","lpe")

## Hist 4
#h_AllaQGCPar_initialize = r.TH1F("h_AllaQGCPar_initialize","",20,0,1500)
#h_AllaQGCPar_initialize.SetLineColor(4)
#h_AllaQGCPar_initialize.SetMarkerColor(4)
#leg.AddEntry(h_AllaQGCPar_initialize,"Reweighted SM (Set all Par)","lpe")

## Hist 5
h_SM = r.TH1F("h_SM","",args.nbin,args.xmin,args.xmax)
h_SM.Sumw2()
h_SM.SetLineColor(5)
h_SM.SetMarkerColor(5)
leg.AddEntry(h_SM,"SM","lpe")

# Fill & Draw all 3 histogram from three different trees. Apply weight in aQGC sample only
#tree_OnlyFT1_initialize.Draw("LHE_MothInfo_mtWW>>h_OnlyFT1_initialize","(LHEWeights[491])*(LHE_MothInfo_mtWLep>200 && LHELeptPt>20 && LHE_MothInfo_mtWLep > 20 && LHE_MothInfo_Iqrk0_pt > 20)")
print "reading tree : 1"
aQGC = args.tree_var+">>h_aQGC_initialize"
Reweight = args.tree_var+">>h_OnlyFT1_initialize"
tree_OnlyFT1_initialize.Draw(aQGC,"59.0*0.2223","")
tree_OnlyFT1_initialize.Draw(Reweight,"59.0*0.223*LHEWeights[181]/LHEWeights[0]","")
#tree_OnlyFT1_initialize.Draw("LHE_MothInfo_mtWLep>>h_aQGC_initialize","59.0*0.2223","")
#tree_OnlyFT1_initialize.Draw("LHE_MothInfo_mtWLep>>h_OnlyFT1_initialize","59.0*0.223*LHEWeights[181]/LHEWeights[0]","")
#print "reading tree : 2"
#tree_AllaQGCPar_initialize.Draw("LHE_MothInfo_mtWLep>>h_AllaQGCPar_initialize","(LHEWeights[491])","")
print "reading tree : 2"
SM = args.tree_var+">>h_SM"
print SM
tree_SM.Draw(SM,"59.0*0.02982","")
#tree_SM.Draw("LHE_MothInfo_mtWLep>>h_SM","59.0*0.02982","")
# Normalize histogram with unity
h_aQGC_initialize.Scale(1.0/h_aQGC_initialize.Integral())
h_OnlyFT1_initialize.Scale(1.0/h_OnlyFT1_initialize.Integral())
#h_AllaQGCPar_initialize.Scale(1.0/h_AllaQGCPar_initialize.Integral())
h_SM.Scale(1.0/h_SM.Integral())

h3 = createRatio(h_SM,h_OnlyFT1_initialize,1)
#h4 = createRatio(h_SM,h_AllaQGCPar_initialize,4)
#h5 = createRatio(h_SM,h_FT0_8e12,2)

canvas, pad1, pad2 = createCanvasPads()

#print "Integral h_OnlyFT1_initialize = ",h_OnlyFT1_initialize.Integral()
#print "Integral h_AllaQGCPar_initialize = ",h_AllaQGCPar_initialize.Integral()
#print "Integral h_SM = ",h_SM.Integral()

# Draw all hitogram using sames.
pad1.cd()
h_OnlyFT1_initialize.Draw()
h_aQGC_initialize.Draw("same")
#h_AllaQGCPar_initialize.Draw("same")
#h_FT0_10e12.Draw("same")
h_SM.Draw("same")

leg.Draw()

pad2.cd()
h3.Draw("ep")
#h4.Draw("ep same")
#h7.Draw("ep same")
l = r.TLine( 0, 1, 2000, 1 )
l.SetLineStyle(3)
l.Draw("same")

#canvas.Draw()
canvas.SaveAs(args.tree_var+"_xsec.png")
#canvas.SaveAs("LHE_MothInfo_mtWLep_xsec.png")
#canvas.SaveAs("mt_plot_Comp_DifferentSM_Range1500_b250_log.pdf")

clock.Stop()

print 'Tree loop profiling stats:'
print 'Real Time used:', clock.RealTime()
print 'CPU Time used:', clock.CpuTime()

