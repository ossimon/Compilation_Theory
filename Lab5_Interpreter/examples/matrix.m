A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(3, 4);
print(D);
D[0, 0] = 42;
print(D);
D[1:3, 2:4] = 7;
print D;
print D[1, 2];
print D[1:3, 1:3];