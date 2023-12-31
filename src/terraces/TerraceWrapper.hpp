#ifndef RAXML_TERRACES_TERRACEWRAPPER_HPP_
#define RAXML_TERRACES_TERRACEWRAPPER_HPP_

#include <terraces/advanced.hpp>
#include <terraces/parser.hpp>
#include <terraces/errors.hpp>

class PartitionedMSA;
class Tree;

class TerraceWrapper
{
public:
  TerraceWrapper(const PartitionedMSA &part_msa, const Tree &tree);
  TerraceWrapper(const std::string &nwk_filename, const std::string &matrix_filename);
  // TerraceWrapper();
  // TerraceWrapper(const terraces::supertree_data &supertree, const terraces::bitmatrix &bm, const terraces::name_map &names, const terraces::index_map &indices);
  // TerraceWrapper(const terraces::supertree_data &supertree, const terraces::bitmatrix &bm, const terraces::name_map &names);
  // TerraceWrapper
  std::uint64_t terrace_size();
  void print_terrace_newick(std::ostream &output);
  void print_terrace_compressed(std::ostream &output);
  void print_terrace(std::ostream &output);

private:
  terraces::bitmatrix _bm;
  terraces::name_map _names;
  terraces::index_map _indices;
  terraces::supertree_data _supertree;
};

#endif /* RAXML_TERRACES_TERRACEWRAPPER_HPP_ */
