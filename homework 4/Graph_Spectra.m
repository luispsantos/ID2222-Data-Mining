clear all
clc
%%
k=4
E=csvread('example1.dat');
algorithm(E, k);
%%
k=2
E=csvread('example2.dat');
algorithm(E, k);
%%


function [clusters, L]=algorithm(E, k)
    % step 1
    A=step1(E);
    figure(1)
    spy(A)
    figure(2)
    plot(graph(A), 'Layout','force');
    %figure(3)
    %h=plot(graph(A), 'Layout','force');
    figure(3)
    h=plot(graph(A),'Layout','force3')

    % step 2
    L=step2(A);

    % step 3
    [V,d]=eigs(L,k);

    % step 4
    Y=V./sum(V.*V,2).^(1/2);

    % step 5
    clusters=kmeans(Y,k);

    % step 6
    cluster_colors=hsv(k);
    for i=1:k
        cluster_members=find(clusters==i);
        highlight(h, cluster_members , 'NodeColor', cluster_colors(i,:))
    end
    figure(4)
    [F_V,~]=eigs(un_normalized_L(A),2,'SA');
    plot(sort(F_V(:,2)),'-*')
    figure(5)
    [F_V,~]=eigs(L,2,'SA');
    plot(sort(F_V(:,2)),'-*')
end

function A=step1(E)
    col1=E(:,1);
    col2=E(:,2);
    max_ids = max(max(col1,col2));
    As= sparse(col1, col2, 1, max_ids, max_ids);
    A= full(adjacency(graph(As)));
end

function L=step2(A)
    D=diag(sum(A,2));
    L=(D^(-1/2)*A*D^(-1/2));
end

function L=un_normalized_L(A)
    D=diag(sum(A,2));
    L=D-A;
end
