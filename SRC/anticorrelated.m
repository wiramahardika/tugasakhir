n = 100;
d=3;

%ANT

data = zeros(n,d);
for i = 1:n
    % mendapatkan dimensi dan nilainya yang akan menjadi patokan
    base = rand;
    basedim = ceil (base / (1 / d));
    data(i, basedim) = rand;
    %generata data
    for dim = 1:d
        if dim ~= basedim
            baseotherdim = 1 - data(i,basedim);
            posneg = rand;
            if posneg <= 0.5
                addsub = -1 * (0.5 - posneg) * 0.2;
            else 
                addsub = (posneg - 0.5) * 0.2;
            end
            data(i, dim) = baseotherdim + addsub;
            if data(i,dim) < 0
                data(i,dim) = 0.0;
            elseif data(i,dim) > 1.0;
                data(i,dim) = 1.0;
            end
        end
    end
end