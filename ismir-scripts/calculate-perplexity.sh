#!/bin/bash
# Run this script from 'scripts' directory of mallet directory


echo 'import all data'
bin/mallet import-dir --input plsqbs/ --output tmp/topic-input-plsqbs.mallet --keep-sequence  --stoplist-file stopch.txt --token-regex '[\p{L}\p{M}]+'

echo 'import held out data '
bin/mallet import-dir --input held-out-data/ --output tmp/topic-input-held.mallet --keep-sequence  --stoplist-file stopch.txt --token-regex '[\p{L}\p{M}]+'
	


# Train LDA model for a range of number of topics
# and calculate perplexity for each
for numtopic in {8..50}
do
	echo -e "#######################################################################"
	echo -e "Iteration: number of topics "$numtopic
	echo -e "#######################################################################"

	# Train LDA model
	bin/mallet train-topics --num-topics $numtopic --input tmp/topic-input-plsqbs.mallet --evaluator-filename tmp/output-evaluator.mallet --num-iterations 100 --show-topics-interval 1000 --alpha 1 --beta .07 --output-doc-topics tmp/doc-topics-plsqbs.txt --output-topic-keys tmp/topic-keys-plsqbs.txt --random-seed 1 --optimize-interval 10 

	
	# Calculate perplexity on test data
	# First calculate document probabilities for each 
	# test document
	bin/mallet evaluate-topics --evaluator tmp/output-evaluator.mallet --input tmp/topic-input-held.mallet --output-doc-probs docprobs.txt
	# Calculate document lengths to calculate perplexity
	bin/mallet run cc.mallet.util.DocumentLengths --input tmp/topic-input-held.mallet > doclengths.txt
	# Calculate perplexity
	docLen=($(cat doclengths.txt))
	docProb=($(cat docprobs.txt))
	logLikelihood=0
	totalWords=0
	for ((i=0; i<${#docProb[@]}; i++))
	do
		logLikelihood=`echo "$logLikelihood + ${docProb[$i]}" | bc -l`
		totalWords=`echo "$totalWords + ${docLen[$i]}" | bc -l`
	done
	perplexity=`echo "e(-1*$logLikelihood / $totalWords)" | bc -l`
	#ppx[$idx]=
	echo $numtopic"	"$perplexity >> perplexity.txt
done
# Write perplexity values to a file
#rm -f perplexity.txt
#for ((i=0; i<${#numTopics[@]}; i++))
#do
#	echo -e ${numTopics[$i]}"\t"${ppx[$i]} >> perplexity.txt
#done

        # Delete intermediate files
 #       rm -f tmp/output-evaluator.mallet
  #      rm -f doclengths.txt
   #     rm -f docprobs.txt


