// Plugin para mostrar o texto central no gráfico (Total)
const textoCentral = {
    id: 'textoCentral',
    beforeDraw(chart, args, options) {
        const { width, height } = chart;
        const ctx = chart.ctx;
        ctx.restore();

        // Texto "Total"
        ctx.font = 'bold 18px sans-serif';
        ctx.fillStyle = '#555';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Total', width / 2, height / 2 - 10);

        // Valor abaixo
        ctx.font = 'bold 20px sans-serif';
        ctx.fillStyle = '#000';
        const total = options.total;
        ctx.fillText(`R$ ${total.toFixed(2)}`, width / 2, height / 2 + 15);

        ctx.save();
    }
};