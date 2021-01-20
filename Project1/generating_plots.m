table = readtable("data");
n = table.voters;
m = table.alternatives; 
condorcet = table.condorcet;
borda_picks_condorcet = table.borda_picks_condorcet; 
plurality_picks_condorcet = table.plurality_picks_condorcet; 
all_agree = table.all_agree; 
borda_and_copeland = table.borda_and_copeland; 
borda_and_plurality = table.borda_and_plurality; 
copeland_and_plurality = table.copeland_and_plurality; 
%% Condorcet percent correct 
scatter3(n,m,condorcet,'filled','m')
xlabel('Number of Voters')
ylabel('Number of Alternatives')
zlabel('Percent Condorcet got Correct')
title('How Often a Condorcet Winner Exists')
view(121,16)
saveas(gcf,"condorcet_winner.png")
%% Borda chooses condorcet
scatter3(n,m,borda_picks_condorcet,'filled','m')
xlabel('Number of Voters')
ylabel('Number of Alternatives') 
zlabel('Percent Borda Picks Condorcet')
title('How Often Borda Picks the Condorcet Winner') 
view(121,16)
saveas(gcf,'borda_picks_condorcet.png')
%% Plurality chooses condorcet
scatter3(n,m,plurality_picks_condorcet,'filled','m')
xlabel('Number of Voters')
ylabel('Number of Alternatives')
zlabel('Percent Plurality Picks Condorcet')
title('How Often Plurality Chooses the Condorcet Winner')
view(121,16)
saveas(gcf,"plurality_picks_condorcet.png") 
%% Percentage All Three  Agree
scatter3(n,m,all_agree,'filled','m')
xlabel("Number of Voters")
ylabel("Number of Alternatives")
zlabel("Percentage All Three Agree")
zlim([0,100])
title("How Often Borda, Copeland, and Plurality Agree with No Condorcet Winner") 
view(161,7)
saveas(gcf,"all_three_agree.png")
%% Percentage borda and copeland agree
scatter3(n,m,borda_and_copeland,'filled','m')
xlabel("Number of Voters") 
ylabel("Number of Alternatives") 
zlabel("Percent Borda and Copeland Agree")
zlim([0,100])
title("How Often Borda and Copeland Agree with No Condorcet Winner") 
view(123,11)
saveas(gcf,"borda_and_copeland.png") 
%% Percentage borda and plurality agree
scatter3(n,m,borda_and_plurality,'filled','m')
xlabel("Number of Voters") 
ylabel("Number of Alternatives") 
zlabel("Percent Borda and Plurality Agree") 
title("How Often Borda and Plurality Agree with No Condorcet Winner") 
view(103,12)
zlim([0,100])
saveas(gcf,"borda_and_plurality.png") 
%% Percentage copeland and plurality agree 
scatter3(n,m,copeland_and_plurality,'filled','m')
xlabel("Number of Voters") 
ylabel("Number of Alternatives") 
zlabel("Percent Copeland and Plurality Agree") 
title("How Often Copeland and Plurality Agree with No Condorcet Winner") 
zlim([0,100])
view(106,12)
saveas(gcf,"copeland_and_plurality.png")