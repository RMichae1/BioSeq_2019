using StatsBase

# load PDF for underlying acids
acid_dist = Dict{String, Float64}("A" => 0.095070,
                          "C" => 0.011560,
                          "D" => 0.051634,
                          "E" => 0.039081,
                          "F" => 0.039081,
                          "G" => 0.073548,
                          "H" => 0.022629,
                          "I" => 0.060123,
                          "K" => 0.043981,
                          "L" => 0.106769,
                          "M" => 0.028008,
                          "N" => 0.039309,
                          "P" => 0.044342,
                          "Q" => 0.044409,
                          "R" => 0.055342,
                          "S" => 0.058097,
                          "T" => 0.053810,
                          "V" => 0.070647,
                          "W" => 0.015378,
                          "Y" => 0.028498)
seq_length = 319
batches = 408
out_file = "random_acid.txt"

# create random string of elements
acid_arr = collect(keys(acid_dist))
@show acid_arr
# call collect to turn Iterator Object to Array
weights = pweights(collect(values(acid_dist)))
@show weights

# write output directly to file so there is no string concat overhead
open(out_file, "w") do f
    for acid=1:batches
        # string join 
        acid_seq = join(sample(acid_arr, weights, seq_length))
        # Concatenate Batch id and weights
        tmp_seq = ">ACID_$acid \n $acid_seq \n"
        @show tmp_seq
        write(f, tmp_seq)
    end
end
