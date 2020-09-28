import ROOT
import sys

infn=sys.argv[1]

inf=ROOT.TFile(infn,"READ")
t=inf.Get("otree")

print "nEvents = ",t.GetEntries()

outf=open("branchlist_nano_selection.txt","w")
brl=t.GetListOfBranches()
for br in brl:
  name=br.GetName()
  outf.write(name+"\n")

outf.close()
