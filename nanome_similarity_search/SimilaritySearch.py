import nanome
import os
from nanome.util import Logs
from .similaritysearch_menu import SimilaritySearchMenu
from .similaritysearch_menu import ErrorOptions
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
 
class SimilaritySearch(nanome.PluginInstance):

    def start(self):
        self._menu = SimilaritySearchMenu(self)
        self._menu.build_menu()
        nanome.util.Logs.debug("similarity search plugin started")
        self.number_of_results = 10
        self.result_list = []
        self.selected_query = None
        self.letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}


    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)
        self._menu._request_refresh()
        nanome.util.Logs.debug("on run called")

    def on_complex_added(self):
        nanome.util.Logs.debug("Complex added: refreshing")
        self.request_refresh()

    def on_complex_removed(self):
        nanome.util.Logs.debug("Complex removed: refreshing")
        self.request_refresh()

    def request_refresh(self):
        self.request_complex_list(self.on_complex_list_received)
        nanome.util.Logs.debug("Complex list requested")
    
    def on_complex_list_received(self, complexes):
        Logs.debug("complex received: ", complexes)
        self._menu.change_complex_list(complexes)

    def update_selected_query(self,complex):
        if complex!= None:
            self.request_complexes([complex.index],self.on_query_received)
        else:
            self.selected_query = None
    
    def on_query_received(self,complex):
        self.selected_query = complex[0]

    def pdb_to_fasta(self,complex):
        fasta_res = ""
        complex_name = complex.full_name
        print("chains are: ",complex.chains)
        print(len(list(complex.chains)))
        for chain in complex.chains:
            if not any(atom.is_het for atom in chain.atoms):
                fasta_res+=(">"+complex_name+":"+chain.name+"\n")
                for residue in [x.type for x in chain.residues ]:
                    if residue in self.letters:
                        fasta_res+=(self.letters[residue])
                fasta_res+=("\n")
        return fasta_res

    def update_error_message(self,option):
        self._menu.update_error_message(option)

    def search_blast(self):
        Logs.debug("blast search test started")
        # with open(os.path.join(os.path.dirname(__file__), "1tyl.fasta"),"r") as file:
        #     fasta_string = file.read()
        # Logs.debug("the fasta string is: ",fasta_string)
        if self.selected_query:
            fasta_string = self.pdb_to_fasta(self.selected_query)
            print(fasta_string)
            result_handle = NCBIWWW.qblast("blastp", "nt", fasta_string)
            print("result handle: ",result_handle)
            Logs.debug("qblast ended")
            for x in range(self.number_of_results):
                Logs.debug("iteration ",x+1,": ")
                if x == 0:
                    try:
                        blast_record = NCBIXML.parse(result_handle)
                        Logs.debug("the #",x+1," result is: ",blast_record)
                        self.result_list.append(blast_record)
                    except:
                        Logs.debug("No result found")
                        break
                        Logs.debug("blast result #1: ",blast_record)
                else:
                    try:
                        blast_record = next(blast_records)
                        self.result_list.append(blast_record)
                        Logs.debug("blast result #",x+1," ",blast_record)
                    except:
                        Logs.debug("No more results")
                        break
        else:
            self.update_error_message(ErrorOptions.unselected)

        self.update_result()

    def update_result(self):
        self._menu.update_result(self.result_list)

def main():
    plugin = nanome.Plugin('Similarity Search', 'A Nanome plugin to do similarity search using BLAST', 'other', False)
    plugin.set_plugin_class(SimilaritySearch)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()
